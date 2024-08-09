CREATE DATABASE IF NOT EXISTS hms;
USE hms;

DROP TABLE IF EXISTS `guests`;
CREATE TABLE `guests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

LOCK TABLES `guests` WRITE;
INSERT INTO `guests` VALUES (1,'Heinrich Klaasen','US','klaasen@csa.com',1231231231,"NYC",'2024-10-14 08:51:19'),(2,'utkarsh','India','ukr@abc.xy',1111111111,"Mumbai",'2024-10-17 05:19:02'),(3,'Jake','NMS','jake0@gmail.com',9191919191,"Vatican",'2024-10-17 06:58:23');
UNLOCK TABLES;


DROP TABLE IF EXISTS `rooms`;
CREATE TABLE `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_no` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `room_type` char(2) DEFAULT NULL,
  `currently_booked` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_no` (`room_no`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

LOCK TABLES `rooms` WRITE;
INSERT INTO `rooms` VALUES (1,1,4500,'D',0,'2021-10-15 07:05:03'),(2,2,3402,'D',0,'2021-10-16 10:38:49'),(3,3,2300,'D',0,'2021-10-17 05:15:29'),(4,4,3124,'N',0,'2021-10-17 05:15:38'),(5,5,3241,'N',0,'2021-10-17 05:16:09'),(6,6,4000,'D',0,'2021-10-17 05:16:33'),(7,7,2341,'D',0,'2021-10-17 05:17:29'),(8,8,3045,'D',0,'2021-10-17 06:57:46');
UNLOCK TABLES;

DROP TABLE IF EXISTS `login`;
CREATE TABLE `login` (
  `username` varchar(15) NOT NULL,
  `password` varchar(10) NOT NULL,
  `sec_que` varchar(100) NULL,
  `sec_ans` varchar(30) NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `login` WRITE;
INSERT INTO `login` VALUES ('username','password', NULL, NULL,'2021-08-13 01:34:25');
UNLOCK TABLES;

DROP TABLE IF EXISTS `reservations`;
CREATE TABLE `reservations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `g_id` int(11) DEFAULT NULL,
  `r_date` datetime DEFAULT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `meal` tinyint(1) DEFAULT NULL,
  `r_id` int(11) DEFAULT NULL,
  `r_type` char(2) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_guests` (`g_id`),
  KEY `FK_rooms` (`r_id`),
  CONSTRAINT `FK_guests` FOREIGN KEY (`g_id`) REFERENCES `guests` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_rooms` FOREIGN KEY (`r_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

LOCK TABLES `reservations` WRITE;
INSERT INTO `reservations` VALUES (1,1,'2021-10-15 00:00:00','2021-10-15 00:00:00','2021-10-15 00:00:00',0,3,'B','2021-10-15 07:05:05'),(2,2,NULL,'2021-10-17 05:33:05',NULL,1,1,NULL,'2021-10-17 05:33:05');
UNLOCK TABLES;
