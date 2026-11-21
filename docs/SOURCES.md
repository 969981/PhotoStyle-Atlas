# 上游来源与许可证

本项目同步的是可安装 Skills 及必要依赖，不是整仓库 1:1 克隆所有案例图库和开发历史。
各上游原始版权声明请以 LICENSES/ 与各 Skill 内的 LICENSE/NOTICE 为准。

| 源仓库 | 独立 Skills | 上游版本 Commit | 授权 |
| --- | ---: | --- | --- |
| [GZ-L/photo-to-poster-skills](https://github.com/GZ-L/photo-to-poster-skills) | 14 | [268ee78460ab](https://github.com/GZ-L/photo-to-poster-skills/commit/268ee78460ab5592167082d0501b7834f2e5b676) | MIT |
| [Vieeeeeee/wibi-style](https://github.com/Vieeeeeee/wibi-style) | 52 | [c063b052fc27](https://github.com/Vieeeeeee/wibi-style/commit/c063b052fc275bea92dd4cc15e509157cffa310c) | Wibi Personal Non-Commercial 1.0 + MIT tooling |
| [jyi06/image-style-transfer](https://github.com/jyi06/image-style-transfer) | 1 | [639215b3c5e8](https://github.com/jyi06/image-style-transfer/commit/639215b3c5e83ba60daa16aee3e2546ece07d78e) | MIT |
| [yanliudesign/mono-color-skill](https://github.com/yanliudesign/mono-color-skill) | 1 | [c8ff70597dde](https://github.com/yanliudesign/mono-color-skill/commit/c8ff70597ddedcd65f21a0b528f6a70c35690b0a) | MIT |
| [jiahuiqu17/paper-signal](https://github.com/jiahuiqu17/paper-signal) | 4 | [7567ff05f93f](https://github.com/jiahuiqu17/paper-signal/commit/7567ff05f93fe525bf886b3a0dce36903ab8c43b) | MIT |
| [SARSfang/photo-to-minimal-form-poster](https://github.com/SARSfang/photo-to-minimal-form-poster) | 1 | [0a294eaef8e7](https://github.com/SARSfang/photo-to-minimal-form-poster/commit/0a294eaef8e7053666a000a05676b1e8cdff7449) | MIT |
| [gaoren7716-lab/anime-image-restyle-skill](https://github.com/gaoren7716-lab/anime-image-restyle-skill) | 1 | [404ac129e22d](https://github.com/gaoren7716-lab/anime-image-restyle-skill/commit/404ac129e22d220ae69bc43db6b434fdfaa95a4b) | MIT |
| [GuohongLi/muse-skills](https://github.com/GuohongLi/muse-skills) | 3 | [401744b6eaf1](https://github.com/GuohongLi/muse-skills/commit/401744b6eaf1b4dad0f10846d4df998951215a43) | MIT |
| [eamonboyle/computer-use-photo-editing-skills](https://github.com/eamonboyle/computer-use-photo-editing-skills) | 5 | [d6405d6dbc32](https://github.com/eamonboyle/computer-use-photo-editing-skills/commit/d6405d6dbc32db8d005e2146ea3591cec9a19a83) | MIT |
| [aipiratesMunich/photo-editing-craft](https://github.com/aipiratesMunich/photo-editing-craft) | 1 | [448f34fc8e53](https://github.com/aipiratesMunich/photo-editing-craft/commit/448f34fc8e53f406e8c002cf061c0471fe6030c2) | MIT |
| [howardz27/poster-generator-skill](https://github.com/howardz27/poster-generator-skill) | 1 | [fa2a40bf0943](https://github.com/howardz27/poster-generator-skill/commit/fa2a40bf0943c14dbcf2dfd86a2efe66fa8b4cbc) | MIT |
| [Serennity007/awesome-creative-skills](https://github.com/Serennity007/awesome-creative-skills) | 0 | [2457f05dd3b0](https://github.com/Serennity007/awesome-creative-skills/commit/2457f05dd3b0c6cf830fabe2ebea719402dacdd2) | MIT |
| [moskoo/xxg-portrait-rebuild-light](https://github.com/moskoo/xxg-portrait-rebuild-light) | 1 | [39b1ffd21248](https://github.com/moskoo/xxg-portrait-rebuild-light/commit/39b1ffd21248fd22e2d4e3075ec0ca0989236dd9) | MIT |
| [L-Trunks/ai-portrait-light](https://github.com/L-Trunks/ai-portrait-light) | 1 | [4def521eed57](https://github.com/L-Trunks/ai-portrait-light/commit/4def521eed57a08e37ac90ac953e7fe42a952b2d) | CC BY 4.0 documents/images (licensed examples 01-10) + MIT code |
| [grapeot/genai_portrait_skill](https://github.com/grapeot/genai_portrait_skill) | 1 | [45bbea31e1c8](https://github.com/grapeot/genai_portrait_skill/commit/45bbea31e1c8dcc9fd839ad9d256ab78e4385763) | MIT |
| [robyboy888/photo-retouch-pro](https://github.com/robyboy888/photo-retouch-pro) | 1 | [21bc81931b63](https://github.com/robyboy888/photo-retouch-pro/commit/21bc81931b63061aa44dacf61106fda3e08c105e) | MIT |

## 新增人像修图的授权与依赖

- **XXG Portrait Rebuild Light**：上游 MIT；主要是光影工作流与核对脚本，需外部实际修图后端。
- **AI Portrait Light**：上游文本/图片 CC BY 4.0，代码 MIT；署名与原有 CC BY 4.0 条款必须保留；镜像仅保存其许可明确覆盖的早期示例预览。最新示例图从上游获取。
- **GenAI Portrait Skill**：上游 MIT；其 Python CLI 依赖须另行安装，生成式编辑可能需要 OpenAI/Gemini 等服务凭据。
- **Roby Photo Retouch Pro**：MIT，十种人像和照片精修模式，需宿主编辑后端。
- **Atlas Portrait Suite**：本仓库自编完整 Skill，沿用仓库 MIT，独立本地清单，不由上游同步覆盖。
- **其他外部候选**：x-rush、hotcoffeeshake、eachlabs、tuxiuxiu 未发现明确项目授权，暂不镜像；AInVFX 为 Apache-2.0 ComfyUI 视频特效工具。

## Wibi Style 特殊条款

上游对自动化工具使用 MIT 条款，对原创视觉规则与提示词使用个人非商业许可；各目录保留作者署名、LICENSE 和 NOTICE。第三方图片与字体可能各有额外要求。
用户表示已经获得导入许可，但公开镜像不等于项目向第三人发放商业使用权。

本项目不是上述上游项目的官方发行版。
