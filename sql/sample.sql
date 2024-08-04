use uk;
-- Creating Guests table
DROP TABLE IF EXISTS `guest1`;
CREATE TABLE `guest1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  `phone` bigint DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


INSERT INTO `guest1` (`name`, `address`, `email_id`, `phone`, `city`) VALUES
('John Doe', '123 Main St', 'johndoe@example.com', 1234567890, 'New York'),
('Jane Smith', '456 Elm St', 'janesmith@example.com', 2345678901, 'Los Angeles'),
('Robert Brown', '789 Oak St', 'robertbrown@example.com', 3456789012, 'Chicago'),
('Emily Davis', '321 Pine St', 'emilydavis@example.com', 4567890123, 'Houston'),
('Michael Wilson', '654 Maple St', 'michaelwilson@example.com', 5678901234, 'Phoenix'),
('Sarah Johnson', '987 Cedar St', 'sarahjohnson@example.com', 6789012345, 'Philadelphia'),
('David Martinez', '159 Birch St', 'davidmartinez@example.com', 7890123456, 'San Antonio'),
('Laura Garcia', '753 Walnut St', 'lauragarcia@example.com', 8901234567, 'San Diego'),
('James Rodriguez', '258 Spruce St', 'jamesrodriguez@example.com', 9012345678, 'Dallas'),
('Linda Anderson', '456 Cherry St', 'lindaanderson@example.com', 1012345678, 'San Jose');

select * from guest1

-- creating rooms table
DROP TABLE IF EXISTS `rooms1`;
CREATE TABLE `rooms1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_no` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `room_type` char(2) DEFAULT NULL,
  `currently_booked` tinyint DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_no` (`room_no`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

INSERT INTO `rooms1` (`room_no`, `price`, `room_type`, `currently_booked`) VALUES
(101, 5000, 'D', 0),
(102, 6000, 'N', 1),
(103, 7000, 'D', 0),
(104, 8000, 'N', 1),
(105, 9000, 'D', 0),
(106, 10000, 'N', 1),
(107, 5500, 'D', 0),
(108, 6500, 'N', 1),
(109, 7500, 'D', 0),
(110, 8500, 'N', 1);

select * from rooms1

-- creating Login table
DROP TABLE IF EXISTS `login1`;
CREATE TABLE `login1` (
  `username` varchar(15) NOT NULL,
  `password` varchar(10) NOT NULL,
  `sec_que` varchar(100) NULL,
  `sec_ans` varchar(30) NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

insert into login1(username, password)values('imukr','pass');

select * from login1;

-- creating reservation table
DROP TABLE IF EXISTS `reservations1`;
CREATE TABLE `reservations1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `g_id` int DEFAULT NULL,
  `r_date` datetime DEFAULT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `meal` tinyint DEFAULT NULL,
  `r_id` int DEFAULT NULL,
  `r_type` char(2) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_guests` (`g_id`),
  KEY `FK_rooms` (`r_id`),
  CONSTRAINT `FK_guests` FOREIGN KEY (`g_id`) REFERENCES `guest1` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_rooms` FOREIGN KEY (`r_id`) REFERENCES `rooms1` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

INSERT INTO `reservations1` (`g_id`, `r_date`, `check_in`, `check_out`, `meal`, `r_id`, `r_type`) VALUES
(1, '2024-08-01 14:00:00', '2024-08-01 15:00:00', '2024-08-05 11:00:00', 1, 1, 'D'),
(2, '2024-08-02 14:00:00', '2024-08-02 15:00:00', '2024-08-06 11:00:00', 0, 2, 'N'),
(3, '2024-08-03 14:00:00', '2024-08-03 15:00:00', '2024-08-07 11:00:00', 1, 3, 'D'),
(4, '2024-08-04 14:00:00', '2024-08-04 15:00:00', '2024-08-08 11:00:00', 0, 4, 'N'),
(5, '2024-08-05 14:00:00', '2024-08-05 15:00:00', '2024-08-09 11:00:00', 1, 5, 'D'),
(6, '2024-08-06 14:00:00', '2024-08-06 15:00:00', '2024-08-10 11:00:00', 0, 6, 'N'),
(7, '2024-08-07 14:00:00', '2024-08-07 15:00:00', '2024-08-11 11:00:00', 1, 7, 'D'),
(8, '2024-08-08 14:00:00', '2024-08-08 15:00:00', '2024-08-12 11:00:00', 0, 8, 'N'),
(9, '2024-08-09 14:00:00', '2024-08-09 15:00:00', '2024-08-13 11:00:00', 1, 9, 'D'),
(10, '2024-08-10 14:00:00', '2024-08-10 15:00:00', '2024-08-14 11:00:00', 0, 10, 'N');

select * from reservations1
