CREATE DATABASE IF NOT EXISTS smartstay;
USE smartstay;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

LOCK TABLES `guests` WRITE;
INSERT INTO `guests` VALUES (1,'Heinrich Klaasen','1024 Lucia Winset','klaasen@csa.com',7845215223,"NYC",'2024-07-14 08:51:19'),(2,'Utkarsh Roy','East Lane 77','utkarsh.roy25@gmail.com',8754562204,"Mumbai",'2024-07-17 05:19:02'),(3,'Jake','St. Peters 2029','jake0@gmail.com',9191919191,"Vatican",'2024-07-17 06:58:23');
INSERT INTO `guests` (`name`, `address`, `email_id`, `phone`, `city`)
VALUES
('Aarav Mehta', '123 Park Street', 'aarav.mehta@gmail.com', 919876543210, 'Mumbai'),
('Kanishk Mandrelia', '1414 Bhayandar Street', 'kanishkmandrelia@gmail.com', 120198765432, 'Mumbai'),
('Priya Sharma', '456 Rose Avenue', 'priya.sharma@gmail.com', 918765432109, 'Delhi'),
('Jane Smith', '1515 Oak Avenue', 'jane.smith@gmail.com', 121209876543, 'Los Angeles'),
('Raj Patel', '789 Oak Lane', 'raj.patel@gmail.com', 917654321098, 'Ahmedabad'),
('Michael Johnson', '1616 Maple Lane', 'michael.johnson@gmail.com', 122319876543, 'Chicago'),
('Sanya Malhotra', '101 Maple Drive', 'sanya.malhotra@gmail.com', 916543210987, 'Bangalore'),
('Emily Davis', '1717 Rose Road', 'emily.davis@gmail.com', 123429876543, 'Houston'),
('Ankit Singh', '202 Pine Road', 'ankit.singh@gmail.com', 915432109876, 'Chennai'),
('Chris Brown', '1818 Elm Drive', 'chris.brown@gmail.com', 124539876543, 'Miami'),
('Isha Nair', '303 Cedar Street', 'isha.nair@gmail.com', 914321098765, 'Kolkata'),
('Olivia Wilson', '1919 Cedar Way', 'olivia.wilson@gmail.com', 125649876543, 'Seattle'),
('Rohan Desai', '404 Elm Lane', 'rohan.desai@gmail.com', 913210987654, 'Hyderabad'),
('Liam Martinez', '2020 Birch Lane', 'liam.martinez@gmail.com', 126759876543, 'San Francisco'),
('Nikita Kapoor', '505 Birch Way', 'nikita.kapoor@gmail.com', 912109876543, 'Pune'),
('Sophia Lopez', '2121 Pine Drive', 'sophia.lopez@gmail.com', 127869876543, 'Austin'),
('Aditya Verma', '606 Cedar Street', 'aditya.verma@gmail.com', 911098765432, 'Jaipur'),
('Noah Gonzalez', '2222 Oak Road', 'noah.gonzalez@gmail.com', 128979876543, 'Dallas'),
('Pooja Reddy', '707 Ash Lane', 'pooja.reddy@gmail.com', 910987654321, 'Hyderabad'),
('Ava Clark', '2323 Maple Avenue', 'ava.clark@gmail.com', 129089876543, 'Denver'),
('Arjun Rao', '808 Oak Drive', 'arjun.rao@gmail.com', 919098765432, 'Bangalore'),
('Mason Perez', '2424 Rose Street', 'mason.perez@gmail.com', 120198765432, 'San Diego'),
('Meera Gupta', '909 Pine Avenue', 'meera.gupta@gmail.com', 918987654321, 'Chennai'),
('Ella Anderson', '2525 Elm Lane', 'ella.anderson@gmail.com', 121309876543, 'Portland'),
('Shivam Shah', '1010 Maple Street', 'shivam.shah@gmail.com', 917876543210, 'Mumbai'),
('Jacob Thompson', '2626 Cedar Avenue', 'jacob.thompson@gmail.com', 122419876543, 'Las Vegas'),
('Riya Kulkarni', '1111 Rose Lane', 'riya.kulkarni@gmail.com', 916765432109, 'Pune'),
('Mia Robinson', '2727 Birch Way', 'mia.robinson@gmail.com', 123529876543, 'Phoenix'),
('Manish Joshi', '1212 Elm Road', 'manish.joshi@gmail.com', 915654321098, 'Jaipur'),
('Lucas White', '2828 Pine Street', 'lucas.white@gmail.com', 124639876543, 'Boston'),
('Anjali Singh', '1313 Cedar Avenue', 'anjali.singh@gmail.com', 914543210987, 'Kolkata'),
('Ryan Patel', '2929 Oak Avenue', 'ryan.patel@gmail.com', 911198765432, 'Ahmedabad'),
('Amelia Taylor', '3030 Maple Lane', 'amelia.taylor@gmail.com', 910109876543, 'Los Angeles'),
('Henry Garcia', '3131 Rose Road', 'henry.garcia@gmail.com', 929198765432, 'Miami'),
('Aarushi Iyer', '3232 Elm Drive', 'aarushi.iyer@gmail.com', 919209876543, 'Chennai'),
('Ethan Allen', '3333 Cedar Street', 'ethan.allen@gmail.com', 121098765432, 'Philadelphia'),
('Ivy Chopra', '3434 Oak Way', 'ivy.chopra@gmail.com', 918219876543, 'Delhi'),
('David Walker', '3535 Maple Drive', 'david.walker@gmail.com', 917098765432, 'Chicago'),
('Zara Khan', '3636 Pine Avenue', 'zara.khan@gmail.com', 916989876543, 'Mumbai'),
('William King', '3737 Rose Street', 'william.king@gmail.com', 929309876543, 'San Francisco'),
('Neha Bansal', '3838 Elm Lane', 'neha.bansal@gmail.com', 915879876543, 'Hyderabad'),
('Olivia Green', '3939 Cedar Avenue', 'olivia.green@gmail.com', 914769876543, 'Boston'),
('Karan Jain', '4040 Birch Way', 'karan.jain@gmail.com', 913659876543, 'Jaipur'),
('Emma Watson', '4141 Oak Drive', 'emma.watson@gmail.com', 912549876543, 'New York'),
('Amitabh Thakur', '4242 Pine Lane', 'amitabh.thakur@gmail.com', 911439876543, 'Delhi'),
('Sophia Turner', '4343 Maple Avenue', 'sophia.turner@gmail.com', 910329876543, 'Los Angeles'),
('Ravi Subramanian', '4444 Cedar Street', 'ravi.subramanian@gmail.com', 919098765431, 'Chennai'),
('Lily Johnson', '4545 Rose Lane', 'lily.johnson@gmail.com', 928219876543, 'Seattle'),
('Vikram Chauhan', '4646 Oak Road', 'vikram.chauhan@gmail.com', 917109876543, 'Mumbai'),
('Ella Brown', '4747 Birch Way', 'ella.brown@gmail.com', 916009876543, 'Portland'),
('Aryan Gupta', '4848 Pine Street', 'aryan.gupta@gmail.com', 915119876543, 'Pune'),
('Mia Wilson', '4949 Maple Lane', 'mia.wilson@gmail.com', 914229876543, 'San Diego'),
('Rishi Sinha', '5050 Cedar Avenue', 'rishi.sinha@gmail.com', 913339876543, 'Hyderabad'),
('Sophia Davis', '5151 Rose Road', 'sophia.davis@gmail.com', 912449876543, 'Miami'),
('Nikhil Desai', '5252 Oak Drive', 'nikhil.desai@gmail.com', 911559876543, 'Ahmedabad'),
('Lily Martinez', '5353 Elm Lane', 'lily.martinez@gmail.com', 929669876543, 'Dallas'),
('Rekha Sharma', '5454 Birch Way', 'rekha.sharma@gmail.com', 918789876543, 'Bangalore'),
('Amelia White', '5555 Maple Avenue', 'amelia.white@gmail.com', 917659876543, 'Austin'),
('Ishaan Kapoor', '5656 Cedar Street', 'ishaan.kapoor@gmail.com', 916549876543, 'Jaipur'),
('Charlotte Taylor', '5757 Rose Lane', 'charlotte.taylor@gmail.com', 915439876543, 'Los Angeles'),
('Rohan Nair', '5858 Oak Drive', 'rohan.nair@gmail.com', 914329876543, 'Kolkata'),
('Isabella Allen', '5959 Elm Road', 'isabella.allen@gmail.com', 913219876543, 'San Francisco'),
('Krishna Iyer', '6060 Birch Way', 'krishna.iyer@gmail.com', 912109876543, 'Chennai'),
('Mason Miller', '6161 Maple Street', 'mason.miller@gmail.com', 911009876543, 'Denver'),
('Ananya Patel', '6262 Cedar Avenue', 'ananya.patel@gmail.com', 920198765432, 'Pune'),
('Sophia Lee', '6363 Pine Street', 'sophia.lee@gmail.com', 921309876543, 'Chicago'),
('Manoj Verma', '6464 Oak Lane', 'manoj.verma@gmail.com', 922419876543, 'Jaipur'),
('Lily Clark', '6565 Maple Avenue', 'lily.clark@gmail.com', 923529876543, 'Houston'),
('Ravi Shah', '6666 Rose Street', 'ravi.shah@gmail.com', 924639876543, 'Bangalore'),
('Sophia Martinez', '6767 Cedar Avenue', 'sophia.martinez@gmail.com', 925749876543, 'Seattle'),
('Varun Agarwal', '6868 Oak Drive', 'varun.agarwal@gmail.com', 926859876543, 'Mumbai'),
('Grace Hernandez', '6969 Birch Way', 'grace.hernandez@gmail.com', 927969876543, 'New York'),
('Arun Mehta', '7070 Maple Lane', 'arun.mehta@gmail.com', 929079876543, 'Delhi'),
('Zara Smith', '7171 Cedar Street', 'zara.smith@gmail.com', 930189876543, 'San Francisco'),
('Kunal Reddy', '7272 Rose Lane', 'kunal.reddy@gmail.com', 931299876543, 'Hyderabad'),
('Sophia Anderson', '7373 Oak Road', 'sophia.anderson@gmail.com', 932409876543, 'Portland'),
('Vivek Jain', '7474 Maple Street', 'vivek.jain@gmail.com', 933519876543, 'Jaipur'),
('Emma Martinez', '7575 Cedar Avenue', 'emma.martinez@gmail.com', 934629876543, 'Chicago'),
('Riya Gupta', '7676 Birch Way', 'riya.gupta@gmail.com', 935739876543, 'Kolkata'),
('Mason Johnson', '7777 Maple Lane', 'mason.johnson@gmail.com', 936849876543, 'Los Angeles'),
('Aditi Singh', '7878 Rose Street', 'aditi.singh@gmail.com', 937959876543, 'Pune'),
('Olivia Brown', '7979 Oak Lane', 'olivia.brown@gmail.com', 929069876543, 'Dallas'),
('Rahul Joshi', '8080 Cedar Way', 'rahul.joshi@gmail.com', 919309876543, 'Ahmedabad'),
('Liam Robinson', '8181 Birch Way', 'liam.robinson@gmail.com', 918409876543, 'Denver'),
('Nikita Nair', '8282 Maple Avenue', 'nikita.nair@gmail.com', 927609876543, 'Chennai'),
('Isabella Thompson', '8383 Rose Lane', 'isabella.thompson@gmail.com', 926709876543, 'San Diego'),
('Amit Deshmukh', '8484 Oak Drive', 'amit.deshmukh@gmail.com', 935909876543, 'Mumbai'),
('Mia Garcia', '8585 Cedar Avenue', 'mia.garcia@gmail.com', 925009876543, 'Seattle'),
('Karthik Sinha', '8686 Birch Way', 'karthik.sinha@gmail.com', 934209876543, 'Bangalore'),
('Sophia Gonzalez', '8787 Maple Lane', 'sophia.gonzalez@gmail.com', 923309876543, 'Los Angeles'),
('Rishi Reddy', '8888 Pine Street', 'rishi.reddy@gmail.com', 912409876543, 'Hyderabad'),
('Ava Harris', '8989 Oak Avenue', 'ava.harris@gmail.com', 911509876543, 'Portland'),
('Neha Kapoor', '9090 Cedar Street', 'neha.kapoor@gmail.com', 920609876543, 'Delhi'),
('Ethan Wilson', '9191 Rose Lane', 'ethan.wilson@gmail.com', 919709876543, 'San Francisco'),
('Rohit Agarwal', '9292 Birch Way', 'rohit.agarwal@gmail.com', 918809876543, 'Pune'),
('Sophia Allen', '9393 Maple Drive', 'sophia.allen@gmail.com', 917909876543, 'Chicago'),
('Ritika Joshi', '9494 Oak Street', 'ritika.joshi@gmail.com', 927019876543, 'Mumbai'),
('Liam Martinez', '9595 Cedar Lane', 'liam.martinez@gmail.com', 926119876543, 'Los Angeles'),
('Ishaan Sharma', '9696 Pine Way', 'ishaan.sharma@gmail.com', 925229876543, 'Jaipur'),
('Sophia Davis', '9797 Birch Road', 'sophia.davis@gmail.com', 924339876543, 'Seattle'),
('Manisha Singh', '9898 Maple Lane', 'manisha.singh@gmail.com', 923449876543, 'Bangalore'),
('Lucas Clark', '9999 Oak Street', 'lucas.clark@gmail.com', 922559876543, 'Hyderabad'),
('Ananya Reddy', '1010 Birch Avenue', 'ananya.reddy@gmail.com', 921669876543, 'Pune'),
('Olivia Harris', '1020 Cedar Drive', 'olivia.harris@gmail.com', 920779876543, 'Chicago'),
('Kunal Kapoor', '1030 Maple Road', 'kunal.kapoor@gmail.com', 919889876543, 'Delhi'),
('Aarav Sinha', '1040 Oak Lane', 'aarav.sinha@gmail.com', 918999876543, 'Kolkata'),
('Emma Smith', '1050 Cedar Avenue', 'emma.smith@gmail.com', 918109876543, 'Miami'),
('Rohan Iyer', '1060 Birch Way', 'rohan.iyer@gmail.com', 917219876543, 'Chennai'),
('Sophia Thompson', '1070 Maple Drive', 'sophia.thompson@gmail.com', 916329876543, 'Houston'),
('Aditya Desai', '1080 Oak Street', 'aditya.desai@gmail.com', 915439876543, 'Jaipur'),
('Amelia Brown', '1090 Pine Avenue', 'amelia.brown@gmail.com', 914549876543, 'Seattle'),
('Aryan Verma', '1100 Birch Way', 'aryan.verma@gmail.com', 913659876543, 'Bangalore'),
('Sophia White', '1110 Maple Lane', 'sophia.white@gmail.com', 912769876543, 'Portland'),
('Nikhil Agarwal', '1120 Cedar Street', 'nikhil.agarwal@gmail.com', 911879876543, 'Mumbai'),
('Isabella Harris', '1130 Oak Avenue', 'isabella.harris@gmail.com', 920989876543, 'Los Angeles'),
('Ravi Mehta', '1140 Birch Drive', 'ravi.mehta@gmail.com', 910099876543, 'Hyderabad'),
('Sophia Clark', '1150 Maple Road', 'sophia.clark@gmail.com', 929209876543, 'Chicago'),
('Karthik Patel', '1160 Oak Lane', 'karthik.patel@gmail.com', 918309876543, 'Ahmedabad'),
('Sophia Lee', '1170 Cedar Way', 'sophia.lee@gmail.com', 927419876543, 'New York');
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

LOCK TABLES `rooms` WRITE;
INSERT INTO `rooms` VALUES (1,1,5500,'D',0,'2024-10-15 07:05:03'),(2,2,6402,'D',0,'2024-10-16 10:38:49'),(3,3,5300,'D',0,'2024-10-17 05:15:29'),(4,4,5124,'N',0,'2024-10-17 05:15:38'),(5,5,5241,'N',0,'2024-10-17 05:16:09'),(6,6,6000,'D',0,'2024-10-17 05:16:33'),(7,7,5341,'D',0,'2024-10-17 05:17:29'),(8,8,5045,'D',0,'2024-10-17 06:57:46');
INSERT INTO `rooms` (`id`, `room_no`, `price`, `room_type`, `currently_booked`)
VALUES
-- Room IDs from 9 to 30, Room Type 'N', Price between 5000 and 7000
(9, 9, 5500, 'N', 0),
(10, 10, 6100, 'N', 0),
(11, 11, 5200, 'N', 0),
(12, 12, 6800, 'N', 0),
(13, 13, 7000, 'N', 0),
(14, 14, 5400, 'N', 0),
(15, 15, 5900, 'N', 0),
(16, 16, 6700, 'N', 0),
(17, 17, 6100, 'N', 0),
(18, 18, 6900, 'N', 0),
(19, 19, 5300, 'N', 0),
(20, 20, 6200, 'N', 0),
(21, 21, 5800, 'N', 0),
(22, 22, 6500, 'N', 0),
(23, 23, 6400, 'N', 0),
(24, 24, 5000, 'N', 0),
(25, 25, 6600, 'N', 0),
(26, 26, 6800, 'N', 0),
(27, 27, 6300, 'N', 0),
(28, 28, 5500, 'N', 0),
(29, 29, 5900, 'N', 0),
(30, 30, 6700, 'N', 0),

-- Room IDs from 31 to 50, Room Type 'D', Price between 6000 and 9000
(31, 31, 7500, 'D', 0),
(32, 32, 8000, 'D', 0),
(33, 33, 8500, 'D', 0),
(34, 34, 9000, 'D', 0),
(35, 35, 8800, 'D', 0),
(36, 36, 7600, 'D', 0),
(37, 37, 6400, 'D', 0),
(38, 38, 7000, 'D', 0),
(39, 39, 7200, 'D', 0),
(40, 40, 6500, 'D', 0),
(41, 41, 8100, 'D', 0),
(42, 42, 8600, 'D', 0),
(43, 43, 6200, 'D', 0),
(44, 44, 8400, 'D', 0),
(45, 45, 6700, 'D', 0),
(46, 46, 7600, 'D', 0),
(47, 47, 9300, 'D', 0),
(48, 48, 7700, 'D', 0),
(49, 49, 6200, 'D', 0),
(50, 50, 7900, 'D', 0);
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
INSERT INTO `login` VALUES ('username','password', NULL, NULL,'2024-08-13 01:34:25');
INSERT INTO `login` VALUES ('imukr','pass', NULL, NULL,'2024-08-13 01:34:25');
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
INSERT INTO `reservations` VALUES (1,1,'2024-10-15 00:00:00','2024-10-15 00:00:00','2024-10-15 00:00:00',0,3,'B','2024-10-15 07:05:05'),(2,2,NULL,'2024-10-17 05:33:05',NULL,1,1,NULL,'2024-10-17 05:33:05');
UNLOCK TABLES;

CREATE TABLE `loyalty` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guest_id` int NOT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`))
  ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
  
  insert into `loyalty`(`guest_id`,`email_id`) values (2,'utkarsh.roy25@gmail.com')
