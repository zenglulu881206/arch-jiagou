// Package sidecar 管理 Python 侧车进程：启动、就绪等待、JSON 调用、退出时关闭。
// 无业务色彩，业务调用写在 logic/<业务>/ 里。
package sidecar

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"time"
)

// Manager 一个侧车进程。port 只监听 127.0.0.1，不对浏览器开放。
type Manager struct {
	dir          string
	port         int
	startTimeout time.Duration
	baseURL      string
	client       *http.Client
	cmd          *exec.Cmd
}

var current *Manager

// New 创建侧车管理器；dir 是侧车代码目录（含 .venv），startTimeout 要覆盖模型加载耗时。
func New(dir string, port int, startTimeout time.Duration) *Manager {
	return &Manager{
		dir:          dir,
		port:         port,
		startTimeout: startTimeout,
		baseURL:      fmt.Sprintf("http://127.0.0.1:%d", port),
		client:       &http.Client{Timeout: 60 * time.Second},
	}
}

// SetDefault 登记全局侧车，供 logic 通过 Default() 调用。
func SetDefault(m *Manager) { current = m }

// Default 返回启动时登记的侧车。
func Default() *Manager { return current }

// Start 拉起侧车并等待 /py/v1/health 返回 healthy=true。
// 端口上已有健康的侧车时直接复用，不再起第二份。
func (m *Manager) Start(ctx context.Context) error {
	if m.healthy(ctx) {
		return nil
	}
	python := filepath.Join(m.dir, ".venv", "bin", "python")
	if runtime.GOOS == "windows" {
		python = filepath.Join(m.dir, ".venv", "Scripts", "python.exe")
	}
	if _, err := os.Stat(python); err != nil {
		return fmt.Errorf("侧车 Python 环境不存在：%s", python)
	}
	installRoot, err := filepath.Abs(filepath.Join(m.dir, ".."))
	if err != nil {
		return err
	}

	m.cmd = exec.Command(python, "-m", "uvicorn", "app.main:app",
		"--host", "127.0.0.1", "--port", fmt.Sprint(m.port))
	m.cmd.Dir = m.dir
	m.cmd.Env = append(os.Environ(),
		fmt.Sprintf("APP_SIDECAR_PORT=%d", m.port),
		"APP_INSTALL_ROOT="+installRoot,
	)
	m.cmd.Stdout = os.Stdout
	m.cmd.Stderr = os.Stderr
	if err := m.cmd.Start(); err != nil {
		return fmt.Errorf("侧车启动失败：%w", err)
	}

	deadline := time.Now().Add(m.startTimeout)
	for time.Now().Before(deadline) {
		if m.healthy(ctx) {
			return nil
		}
		time.Sleep(500 * time.Millisecond)
	}
	_ = m.Stop()
	return fmt.Errorf("侧车在 %s 内未就绪", m.startTimeout)
}

// Stop 关闭本进程拉起的侧车；复用的外部侧车不关。
func (m *Manager) Stop() error {
	if m.cmd == nil || m.cmd.Process == nil {
		return nil
	}
	if runtime.GOOS != "windows" {
		_ = m.cmd.Process.Signal(os.Interrupt)
		done := make(chan error, 1)
		go func() { done <- m.cmd.Wait() }()
		select {
		case <-done:
			return nil
		case <-time.After(5 * time.Second):
		}
	}
	return m.cmd.Process.Kill()
}

// PostJSON 以 JSON 调用侧车接口，响应解到 out；非 200 时返回带响应体的错误（只进日志，不给操作者看）。
func (m *Manager) PostJSON(ctx context.Context, path string, in, out any) error {
	body, err := json.Marshal(in)
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, m.baseURL+path, bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := m.client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("侧车 %s 返回 %d：%s", path, resp.StatusCode, data)
	}
	return json.Unmarshal(data, out)
}

// healthy 探测侧车是否就绪。
func (m *Manager) healthy(ctx context.Context) bool {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, m.baseURL+"/py/v1/health", nil)
	if err != nil {
		return false
	}
	resp, err := (&http.Client{Timeout: 2 * time.Second}).Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	var res struct {
		Healthy bool `json:"healthy"`
	}
	return resp.StatusCode == http.StatusOK && json.NewDecoder(resp.Body).Decode(&res) == nil && res.Healthy
}
