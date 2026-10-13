# Origin 2021 安装与使用

本仓库基于 [Ge-Shun/origin-mcp](https://github.com/Ge-Shun/origin-mcp) 0.1.4，保留 MIT 许可和上游源码。本分支针对 Windows 64 位 Origin 2021 自带 Python 3.8 的兼容问题提供修复。MCP 服务端仍需独立的 Python 3.10+；不要把服务端安装到 Origin 的 Python 3.8 中。

## 安装

先关闭 Origin 中正在运行的旧桥接。以下命令在 PowerShell 中运行：

```powershell
git clone https://github.com/Oxygen-Wang/origin2021mcp.git
cd origin2021mcp
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\origin-mcp.exe install-origin-app --force
.\.venv\Scripts\python.exe scripts\setup_origin2021.py
```

如使用其他 Python 3.10+ 版本，可替换第一条 `py` 命令中的版本。最后一步从 PyPI 下载 CPython 3.8 的 Windows 64 位依赖 wheel，安装到 Start App 内的 `python38-deps`，并对 originpro 的两个模块启用延迟类型注解。无需在 Origin 内运行 pip 或 ensurepip。重新安装 App 会替换 App 文件夹，因此需要再次运行依赖准备脚本。

自定义 App 安装路径时：

```powershell
.\.venv\Scripts\python.exe scripts\setup_origin2021.py --app-dir 'D:\OriginApps\Origin MCP Bridge Start'
```

## 客户端配置

把下面的 Python 路径改成实际虚拟环境的绝对路径，按客户端支持的配置格式添加 stdio MCP 服务：

```json
{
  "mcpServers": {
    "origin": {
      "command": "C:\\path\\to\\origin2021mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "origin_mcp"]
    }
  }
}
```

首次安装后，按 [App 注册说明](origin-ui-buttons.md) 在 Origin 中注册 Start/Stop Apps。每次启动 Origin 后点击 **Origin MCP Bridge Start**；使用 **Origin MCP Bridge Stop** 停止桥接。桥接在 Origin 的 UI 线程中合作式处理请求。

在 PowerShell 中检查：

```powershell
.\.venv\Scripts\origin-mcp.exe status
.\.venv\Scripts\origin-mcp.exe doctor --ping-origin
```

## 已包含的兼容修复

- 在 pip 导入和 ensurepip 执行前包装 Origin 的标准输入输出流。
- 将运行时 `tuple[int, ...]` 类型别名改为 Python 3.8 可用的 `typing.Tuple`，将字典合并改为解包写法。
- 提供严格长度检查的 `zip_compat`，替换桥接路径中 Python 3.8 不支持的 `zip(strict=...)`。
- 两种 App 生成入口均加入私有 `python38-deps` 搜索路径。
- MCP 服务端依赖限定 `mcp<2`，避免上游主版本接口变化。

## Origin 2021 绘图限制

启动兼容修复不代表全部较新 Origin 绘图接口都能在 2021 使用。实际测试中的常见替代方法如下：

- 图形文字对象优先使用 LabTalk `label`；较新的 `GraphObjects.Add` 接口不可用。
- 误差棒可通过 LabTalk `plotxy` 创建，再用 MCP 更新其链接工作表。
- 合并窗口使用 `merge_graph option:=6`，部分符号选项在 Origin 2021 中不可用。
- 页面尺寸按 `page.resx/page.resy` 换算，不直接把英寸赋给打印点单位的页面宽高。

桥接仅监听 `127.0.0.1` 并保留会话令牌认证。不要上传握手文件、令牌、客户端凭据或私人实验工程。可通过 `ORIGIN_MCP_ALLOWED_ROOTS` 限制可读写目录。

## 验证范围

兼容修复曾在本地 Origin 2021 会话中用于更新工作表、读取核对数据、生成单图、合并图及保存工程。独立 Python 3.8 环境用于检查桥接模块导入。本仓库不包含 Origin、依赖 wheel 或实验数据；其他 Origin 版本及未使用过的专用分析工具仍需验证。
