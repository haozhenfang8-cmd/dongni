# 迁移与回退

1. 部署前导出原D1 SQL到离线加密介质，记录Worker版本、D1 Time Travel书签、表计数。
2. 在验证库导入备份并顺序应用0003、0004、0005；已有0001/0002不要重新创建或重复应用。
3. 比较documents、versions、attempts计数和owner ID。比较旧JSON题目总数与questionnaire_questions计数、旧options总数与questionnaire_options计数、答案数与attempt_answers计数。
4. 0004仅新增表和回填，不删除旧列和历史数据。新应用上线后写关系表；历史版本只读，不受后续编辑影响。
5. 旧GitHub账号没有本地密码，不可通过输入旧ID或同名注册直接登录。先注册新账号，经管理员线下核验后使用 /api/admin/claim 关联旧ID，保留审计。
6. 切换前暂停写入，备份最终增量，迁移并部署；抽查成绩和排行榜，恢复写入。
7. 回退时先停止写入。新应用上线后的新数据不在旧JSON快照中，不能直接回滚Worker；应导出新数据保留后恢复迁移前备份到验证库，确认后切换绑定。原库保留不删。

本地 tests/migration.py 已演练旧数据回填、owner不变、历史分数/选项不变、SQL导出恢复。远程D1尚未演练。
