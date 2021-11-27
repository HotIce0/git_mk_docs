# 一、关于 git_mk_docs
通过git管理存储的markdown文档写作管理平台。

# 二、设计
1. 通过git仓库管理文档
2. 文档的更新，通过git仓库的授权进行控制
3. 平台已缓存的文档的查看，通过该平台的权限管理进行控制
   1. 每个仓库支持创建共享仓库(repo_shared)
   2. 每个共享仓库支持设置是否公开或者指定用户可读
4. 支持收藏仓库

## 2.1 关于共享仓库
实际上就是其原仓库的一个本地git仓库备份。只不过当前的分支是由原仓库的管理人员控制的。
这样设计就可以支持类似于，我的文档有V1，V2各个版本对应着不同的分支，或者是tag。

# 三、数据表设计
> 用户表(t_user)
- id
- nick
  - varchar(32)
- email
  - type: varchar(2048)
- username
  - type: varchar(32) 
  - prop: unique
- password
- ssh_key_public
  - type: varchar(4096)
- ssh_key_private
  - type: varchar(4096)
- create_at(date)

> 文档仓库(t_repository)
- id
- user_id
  - ref:t_user(id)
- name
  - type: varchar(32)
- remarks
  - type: varchar(2048)
- git_ssh_url
  - type: varchar(4096)
- create_at:
  - type: date
- update_at
  - type: date
- update_msg
  - type: varchar(4096)

> 共享仓库表(t_repo_shared)
- id
- repo_id
  - ref: t_shared(id)
- user_id
  - ref: t_user(id)
- name
  - type: varchar(32)
- remarks
  - type: varchar(2048)
- branch
  - type: varchar(512)
- create_at
  - type: date
- update_at
  - type: date
- update_msg
  - type: varchar(4096)
    
> 共享仓库读访问权限控制表(t_repo_shared_read_access)
- id
- user_id
  - ref: t_user(id)
- repo_shared_id
  - ref: t_repo_shared(id)
- expired_at
  - type: date

> 共享仓库收藏表(t_repo_shared_star)
- id
- user_id
  - ref: t_user(id)
- repo_shared_id
  - ref: t_repo_shared(id)
- create_at
  - type: date

# 四、各流程
1. 注册
(2) 输入用户表所需内容即可

2. 创建文档仓库
   1. git仓库创建目前自行去仓库创建（并不是很消耗时间）
   2. 输入仓库相关信息
   3. 提交后台后，确认是否有仓库权限
   
3. 文档编辑、编写
    1. 选择分支进行操作
    2. 通过网页端markdown编辑器进行编写（主要需要处理图片，附件的内容转化）

4. 提交变更
   1. 输入commit即可

5. 分支的合并