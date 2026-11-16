# dongni · 懂你

朋友默契测试平台。沿用第一版 React + Vite + TypeScript / Cloudflare Workers + D1 架构（免费 SQLite Durable Object 承担密码计算）。已移除 Auth.js 和全部第三方登录。

**已部署：https://know-me.know-me.workers.dev 。真实线上 API 核心流程已通过；真实手机、微信与无代理大陆网络尚未验证。**

## 本地运行

Node.js 24+、pnpm。

```
pnpm install --store-dir .pnpm-store --config.package-import-method=copy --config.node-linker=hoisted
pnpm test
python tests/migration.py
python scripts/check_data.py
pnpm preview:local
```

访问 http://127.0.0.1:8787 。本地预览使用 `work/preview.sqlite` 持久化数据，通过 Node SQLite 适配器运行同一份 Worker 路由；不代表真实 workerd 性能。`pnpm test` 会构建 `tests/worker.mjs`，预览依赖它。

真实运行时开发：`pnpm build`、`pnpm exec wrangler d1 migrations apply know-me --local`、`pnpm exec wrangler dev`。当前沙箱中 workerd 曾报 SQLITE_CANTOPEN，Node 适配器不应作为正式部署方案。

## 功能

- 自有用户名密码账号，邮箱选填。用户名 NFKC 规范化并按小写唯一。
- Node 原生 scrypt：N=16384、r=8、p=5、随机盐，密码12–128字符；没有降低参数适配免费额度。
- 随机256位会话令牌，数据库只保存 SHA-256；生产 HttpOnly、Secure、SameSite=Strict Cookie；7天有效，退出当前或全部设备。
- 注册只展示一次256位恢复码，数据库仅保存哈希。恢复后轮换恢复码并撤销会话。不发送邮件，不依赖付费认证。
- IP和账号限流、同源写请求、服务端权限和答案校验。
- 实际320条原创中文题目，19类。题干、选项、多个可接受答案独立编辑；分类搜索、收藏、分类均衡随机推荐、同类换题、私有题目、选项批量粘贴、恢复默认、选项上移、题目拖动和按钮排序。
- 数据库草稿及自动保存、预览、发布独立不可变版本、复制分享链接。
- 朋友免注册逐题作答，服务端评分、逐题结果、分类成绩、同分并列排名；创建者逐题正确率与私人答题记录。
- 一个浏览器参与凭证每版本保留一份成绩。相同凭证重试返回首次结果，后续答案不改写分数。刷新通过 Bearer 凭证恢复结果，昵称不作为身份凭证。清除浏览器数据或换设备可再次参与，属于轻量娱乐产品的边界。
- 私有题目自愿投稿，只提交公开题干和选项；管理员审核、理由与日志、撤稿处理、公共题目新增编辑停启用。

## 数据与安全迁移

所有原迁移均保留。0003增加账号、会话与旧身份关联审计；0004将旧问卷JSON拆到逐题和逐选项关系表，将答题JSON拆到逐题回答表；旧快照和旧owner ID不删除。0005扩充题库到320题，不影响已发布版本。

新写入问卷不再将全部内容放在单行：documents/versions.questions只写兼容值 `[]`。实际数据在 questionnaire_questions / questionnaire_options / attempt_answers。正确答案只出现在创建者与已提交且持有结果凭证的答题者接口中。

旧 GitHub ID 不自动转成同名新用户。管理员核验归属后调用 POST `/api/admin/claim`，传入 legacyId、userId，关联documents、versions和submissions，留下 legacy_claims 记录。不能仅凭用户名或邮箱认领旧数据。

迁移前必须导出数据库和记录版本；关闭写入或安排维护窗口；迁移后核对问卷、版本、参与数和抽样答案再切流。详见 docs/MIGRATION.md。不能在未备份的生产库直接尝试迁移。

## Cloudflare 免费部署

1. 注册 Cloudflare Free，不开通付费 Workers。
2. `pnpm exec wrangler login`。
3. `pnpm exec wrangler d1 create know-me`，把返回的database_id写入wrangler.toml。
4. 对已有数据库先备份，再 `pnpm exec wrangler d1 migrations apply know-me --remote`。
5. `pnpm test`，`pnpm exec wrangler deploy`。静态资源与API在同一Worker，使用免费的workers.dev域名。
6. 注册站内管理员账号，使用其稳定用户ID配置 `ADMIN_USER_IDS`，重新部署；不能用昵称或邮箱授权管理员。

不需要OAuth密钥、邮件服务或付费AI。邮箱目前仅为可选资料，密码恢复统一使用一次性恢复码；没有验证过的邮箱不能直接重置密码。

**免费 CPU 实测与处理：** 第一轮将scrypt直接放在普通Worker时，线上采样CPU P99约274ms，虽然请求成功，但超出10ms预算。最终将认证放到Free支持的SQLite Durable Object（AuthService），其默认CPU预算30秒。密码不落DO存储，用户/哈希/会话仍在D1；保留同等scrypt参数。迁移后的短时Worker采样P99约7.3ms、0错误，线上注册登录恢复等核心流程通过。样本较小，不能替代持续负载和极端长问卷测试。

Durable Object 免费额度耗尽会导致服务不可用，不会自动开通Paid。该方案增加一个内部计算绑定，未引入付费认证、第三方登录或额外数据库采购。官方免费DO限制：https://developers.cloudflare.com/durable-objects/platform/limits/ ，定价：https://developers.cloudflare.com/durable-objects/platform/pricing/ 。

官方： https://developers.cloudflare.com/workers/platform/limits/ ，https://developers.cloudflare.com/workers/runtime-apis/nodejs/crypto/ ，https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

## 备份与恢复

```
mkdir backups
pnpm exec wrangler d1 export know-me --remote --output=backups/backup.sql
```

备份包含私密数据和密码哈希，离线加密保存，不提交GitHub。恢复演练导入**新建空的验证库**后核对内容，再切换绑定；不删除或重建原生产库：

```
pnpm exec wrangler d1 create know-me-restore
pnpm exec wrangler d1 execute know-me-restore --remote --file=backups/backup.sql
```

Free D1提供7天Time Travel：`wrangler d1 time-travel info know-me`，恢复操作见官方 https://developers.cloudflare.com/d1/reference/time-travel/ 。恢复旧应用版本时必须同时使用对应备份；新数据不再写入旧JSON列，不能只回滚旧Worker而继续用新数据。

## 测试与剩余工作

详见 docs/TEST_REPORT.md 和 docs/TASKS.md。真实手机、微信内置浏览器、大陆网络、Cloudflare线上长期CPU负载尚未验证，远程导出恢复已演练。当前没有性能测量结论或生产SLA。长问卷已测试2100题拆行存储，仍受D1请求/批处理/结果大小和Worker CPU/内存真实限制，不能声称无限题数无限吞吐。
