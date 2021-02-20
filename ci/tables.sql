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
