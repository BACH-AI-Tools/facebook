# Cherry Studio 配置指南

本文档详细说明如何在 Cherry Studio 中配置和使用 Facebook Scraper MCP 服务器。

## 配置步骤

### 方法1：通过图形界面配置（推荐）

1. **打开 Cherry Studio**

2. **进入MCP设置**
   - 点击右上角的 `设置`（齿轮图标）
   - 在左侧菜单中选择 `模型上下文协议（MCP）` 或 `MCP Servers`

3. **添加新服务器**
   - 点击 `添加服务器` 或 `Add Server` 按钮

4. **填写服务器信息**
   ```
   名称（Name）: facebook-scraper
   
   命令（Command）: C:\Users\Admin\AppData\Local\Programs\Python\Python313\python.exe
   
   参数（Args）: E:\mcp\facebook\server.py
   
   环境变量（Environment Variables）:
     - 键（Key）: RAPIDAPI_KEY
     - 值（Value）: 你的API密钥
   ```

5. **保存并启用**
   - 点击 `保存` 或 `Save`
   - 确保服务器状态为 `已启用`（Enabled）

6. **重启 Cherry Studio**
   - 完全关闭 Cherry Studio
   - 重新打开应用

### 方法2：直接编辑配置文件

1. **找到配置文件位置**
   
   Cherry Studio 的配置文件通常位于：
   
   **Windows:**
   ```
   %APPDATA%\cherry-studio\config.json
   或
   C:\Users\你的用户名\AppData\Roaming\cherry-studio\config.json
   ```
   
   **Mac:**
   ```
   ~/Library/Application Support/cherry-studio/config.json
   ```
   
   **Linux:**
   ```
   ~/.config/cherry-studio/config.json
   ```

2. **编辑配置文件**
   
   用文本编辑器打开配置文件，找到 `mcpServers` 部分（如果没有则创建），添加以下配置：
   
   ```json
   {
     "mcpServers": {
       "facebook-scraper": {
         "command": "C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
         "args": [
           "E:\\mcp\\facebook\\server.py"
         ],
         "env": {
           "RAPIDAPI_KEY": "你的API密钥"
         },
         "disabled": false
       }
     }
   }
   ```
   
   **注意事项：**
   - Windows路径中的反斜杠需要使用双反斜杠 `\\`
   - 确保JSON格式正确（注意逗号和引号）
   - 替换为你的实际路径和API密钥

3. **保存文件并重启 Cherry Studio**

## 验证配置

配置完成后，验证服务器是否正常工作：

1. **查看服务器状态**
   - 在 Cherry Studio 的 MCP 设置页面
   - 查看 `facebook-scraper` 服务器的状态
   - 应该显示为 `运行中`（Running）或 `已连接`（Connected）

2. **测试工具可用性**
   - 在对话中输入：`列出可用的工具`
   - 应该能看到 8 个 Facebook 搜索工具

3. **测试实际调用**
   - 输入：`搜索Tesla的Facebook主页`
   - 服务器应该返回搜索结果

## 使用示例

配置成功后，你可以在对话中使用这些命令：

### 基础搜索
```
搜索纽约的位置信息
查找关于人工智能的视频
搜索最新的科技帖子
```

### 高级搜索
```
帮我搜索特斯拉公司的Facebook主页
查找巴黎附近的餐厅和景点
搜索本周末的音乐会活动
在Facebook群组中搜索编程相关的讨论
```

### 指定参数
```
搜索"机器学习"相关的帖子，限制返回10条结果
查找名为John Smith的Facebook用户
```

## 故障排查

### 问题1：服务器无法启动

**可能原因：**
- Python路径不正确
- server.py路径不正确
- Python依赖未安装

**解决方案：**
```bash
# 验证Python路径
C:\Users\Admin\AppData\Local\Programs\Python\Python313\python.exe --version

# 验证文件存在
dir E:\mcp\facebook\server.py

# 安装依赖
C:\Users\Admin\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r E:\mcp\facebook\requirements.txt
```

### 问题2：API调用失败

**可能原因：**
- RAPIDAPI_KEY 未设置或错误
- API配额已用完
- 未订阅 Facebook Scraper3 API

**解决方案：**
1. 检查 API 密钥是否正确
2. 登录 RapidAPI 查看订阅状态
3. 检查 API 使用配额

### 问题3：工具列表为空

**可能原因：**
- MCP 服务器未正确连接
- Cherry Studio 未正确识别工具

**解决方案：**
1. 检查 Cherry Studio 的 MCP 日志
2. 重启 Cherry Studio
3. 验证配置文件格式是否正确

### 问题4：返回结果为空

**说明：**
这是正常的，可能因为：
- 搜索关键词不够具体
- Facebook 数据访问受限
- API 免费套餐限制

**建议：**
- 使用更具体的搜索关键词
- 考虑升级 API 订阅套餐

## 配置模板

可以直接使用项目根目录的 `cherry-studio-config.json` 文件作为配置模板：

```bash
# 查看配置模板
notepad E:\mcp\facebook\cherry-studio-config.json
```

## 相关链接

- [Cherry Studio 官网](https://github.com/kangfenmao/cherry-studio)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Facebook Scraper3 API](https://rapidapi.com/krasnoludkolo/api/facebook-scraper3/)
- [项目 README](./README.md)

## 支持

如果遇到问题：
1. 查看本文档的故障排查部分
2. 查看 Cherry Studio 的 MCP 日志
3. 检查 server.py 是否能独立运行
4. 提交 Issue 到项目仓库

