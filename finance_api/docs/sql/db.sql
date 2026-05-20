CREATE TABLE platform_users  (
  `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) NULL,
  `email` varchar(128) NULL,
  `password` varchar(128) NOT NULL COMMENT 'md5',
  `role` int(1) NULL COMMENT '1. founder 2.investor 3.fa  4.expert 5.corp 6.gov',
  `status` int(1) NOT NULL DEFAULT 1 COMMENT '1. active, 2. suspended  3.deleted',
  ` is_verified` int(1) NOT NULL DEFAULT 0 COMMENT '0-不实名认证，1实名认证',
  `lang_pref` varchar(5) NULL COMMENT 'zh,en',
  `token_count` int(10) NOT NULL DEFAULT 0 COMMENT 'token数',
  `last_active` datetime NULL COMMENT '最后活跃时间',
  ` created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) COMMENT = '平台用户表';



CREATE TABLE platform_user_profiles  (
  `user_id` int NOT NULL,
  `display_name` varchar(100) NOT NULL COMMENT '显示名',
  `avatar_url` varchar(256) NULL,
  `bio` longtext NULL,
  `city` varchar(20) NULL COMMENT '北京，上海，深圳，广州',
  `skill_tags` varchar(1024) NULL,
  `industry_tags` varchar(1024) NULL,
  `profile_data` varchar(1024) NULL COMMENT '-- 创业者 profile_data 示例:\r\n-- {\r\n--   \"project_name\": \"智链SaaS\",\r\n--   \"funding_stage\": \"angel\",\r\n--   \"funding_need\": 3000000,\r\n--   \"needs\": [\"cofounder\", \"investment\", \"customer\"],\r\n--   \"team_size\": 3\r\n-- }',
  `embedding` varchar(1024) NULL COMMENT '-- pgvector: 档案语义向量',
  `completeness` int(3) NOT NULL COMMENT '档案完整度 0-100',
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) COMMENT = '用户档案表';;


CREATE TABLE platform_user_auth_logs  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `action` varchar(30) NULL COMMENT '- register/login/logout/verify/reset_pwd',
  `ip_addr` varchar(30) NULL,
  `user_agent` varchar(30) NULL,
  `success` int(1) NULL,
  `create_at` datetime NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`)
) comment = '验证日志';

