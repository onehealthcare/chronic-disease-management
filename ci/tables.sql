--
-- Table structure for table `user`
--
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(96) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `bits` bigint(20) unsigned NOT NULL DEFAULT '0',
  `ident` varbinary(100) NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
);

--
-- Table structure for table `user_auth`
--
CREATE TABLE `user_auth` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) NOT NULL,
  `third_party_id` varchar(128) NOT NULL,
  `provider` int NOT NULL,
  `detail_json` blob,
  `access_token` varchar(512),
  `refresh_token` varchar(512),
  `expires_date` datetime,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_third_party_id` (`third_party_id`),
  KEY `idx_provider` (`provider`),
  KEY `idx_status` (`status`)
);

--
-- Table structure for table `chronic_condition_doc_package`
--
CREATE TABLE `chronic_condition_doc_package` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `desc` TEXT NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FULLTEXT (`desc`) WITH PARSER ngram,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
);

--
-- Table structure for table `chronic_condition_doc_package_ident`
--
CREATE TABLE `chronic_condition_doc_package_ident` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `package_id` int(10) unsigned NOT NULL,
  `ident` varchar(256) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_package_id` (`package_id`),
  KEY `idx_status` (`status`)
);

--
-- Table structure for table `user_phone`
--
CREATE TABLE `user_phone` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_phone` (`phone`),
  KEY `idx_status` (`status`)
);

--
-- Table structure for table `chronic_condition_metric`
--
CREATE TABLE `chronic_condition_metric` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `text` varchar(64) NOT NULL,
  `unit` varchar(64) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_status` (`status`)
);

--
-- Table structure for table `chronic_condition_metric_label`
--
CREATE TABLE `chronic_condition_metric_label` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `metric_id` int(10) NOT NULL,
  `name` varchar(64) NOT NULL,
  `text` varchar(64) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_metric_id` (`metric_id`),
  KEY `idx_status` (`status`)
);

--
-- Table structure for table `chronic_condition_user_metric`
--
CREATE TABLE `chronic_condition_user_metric` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) NOT NULL,
  `metric_id` int(10) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_metric_id` (`metric_id`),
  KEY `idx_status` (`status`)
);
