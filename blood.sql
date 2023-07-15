-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: bloodbank
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blood`
--

DROP TABLE IF EXISTS `blood`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood` (
  `B_CODE` int NOT NULL AUTO_INCREMENT,
  `D_ID` int DEFAULT NULL,
  `B_GROUP` varchar(4) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `PACKETS` int DEFAULT NULL,
  PRIMARY KEY (`B_CODE`),
  KEY `FK_1` (`D_ID`),
  KEY `FK_2` (`B_GROUP`),
  CONSTRAINT `FK_1` FOREIGN KEY (`D_ID`) REFERENCES `donor` (`D_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_2` FOREIGN KEY (`B_GROUP`) REFERENCES `bloodbank` (`B_GROUP`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood`
--

LOCK TABLES `blood` WRITE;
/*!40000 ALTER TABLE `blood` DISABLE KEYS */;
INSERT INTO `blood` VALUES (4,1,'A+',1),(5,1,'B+',2),(6,1,'o+',2),(7,1,'o+',12),(8,1,'o+',3),(9,3,'A+',24),(10,3,'B+',1),(12,8,'B+',1),(13,8,'B+',1),(14,8,'B+',12),(16,5,'A+',2),(17,4,'B+',6),(18,4,'o+',10),(19,3,'o+',1),(20,5,'o+',4),(23,5,'o+',2),(24,8,'o+',1);
/*!40000 ALTER TABLE `blood` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bloodbank`
--

DROP TABLE IF EXISTS `bloodbank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloodbank` (
  `B_GROUP` varchar(4) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `TOTAL_PACKETS` int DEFAULT NULL,
  PRIMARY KEY (`B_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloodbank`
--

LOCK TABLES `bloodbank` WRITE;
/*!40000 ALTER TABLE `bloodbank` DISABLE KEYS */;
INSERT INTO `bloodbank` VALUES ('A+',4),('A-',0),('AB+',0),('AB-',0),('B+',0),('B-',0),('O+',1),('O-',0);
/*!40000 ALTER TABLE `bloodbank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `CONTACT_ID` int NOT NULL AUTO_INCREMENT,
  `B_GROUP` varchar(4) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `C_PACKETS` int DEFAULT NULL,
  `F_NAME` varchar(50) DEFAULT NULL,
  `ADRESS` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`CONTACT_ID`),
  KEY `FK_3` (`B_GROUP`),
  CONSTRAINT `FK_3` FOREIGN KEY (`B_GROUP`) REFERENCES `bloodbank` (`B_GROUP`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (108,'A+',1,'obaid','bsent road'),(109,'o+',2,'obaid','bsent road'),(110,'O+',1,'obaid','bsent road'),(111,'o+',5,'hello','vjd'),(112,'A+',1,'obaid','vjd'),(113,'o+',2,'obaid','bsent road'),(114,'A+',3,'raven','vjd'),(115,'o+',5,'raven','vjd'),(116,'B+',1,'obaid','bsent road'),(117,'A+',2,'hello','bsent road'),(118,'A+',1,'raven','bsent road'),(119,'O+',1,'raven','bsent road'),(120,'O+',1,'obaid','vjd'),(121,'O+',1,'obaid','bsent road'),(122,'o+',1,'raven','vjd'),(124,'O+',1,'hello','vjd'),(125,'O+',1,'babu','ndg'),(126,'o+',1,'babu','ndg'),(127,'O+',1,'eswar','ndg'),(128,'B+',2,'obaid',''),(129,'A+',2,'eswar','vijayawada ,arandal peta'),(130,'o+',2,'eswar','ndg'),(131,'A+',2,'datta','vijayawada'),(132,'O+',2,'nagalakshmi','vjd'),(133,'A+',2,'eswar','vijayawada'),(134,'O+',2,'datta','vijayawada'),(135,'O+',2,'babu',''),(136,'O+',4,'hello',''),(137,'A+',2,'datta','anakapally'),(138,'O+',2,'abhi','benz circle'),(139,'O+',2,'a','anakapally'),(140,'O+',2,'raven','vijayawada ,arandal peta'),(141,'O+',2,'b','1234mainroad');
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor` (
  `D_ID` int NOT NULL AUTO_INCREMENT,
  `DNAME` varchar(50) DEFAULT NULL,
  `SEX` varchar(10) DEFAULT NULL,
  `AGE` int DEFAULT NULL,
  `WEIGHT` int DEFAULT NULL,
  `ADDRESS` varchar(150) DEFAULT NULL,
  `DISEASE` varchar(50) DEFAULT NULL,
  `DEMAIL` varchar(100) DEFAULT NULL,
  `mobile_no` varchar(10) DEFAULT NULL,
  `DONOR_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`D_ID`),
  UNIQUE KEY `mobile_no` (`mobile_no`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES `donor` WRITE;
/*!40000 ALTER TABLE `donor` DISABLE KEYS */;
INSERT INTO `donor` VALUES (1,'harry','male',21,60,'vijayawada','No','harry@gmail.com',NULL,'2023-06-17 10:13:03'),(2,'morph','female',24,59,'vijayawada','covid','morph@gmail.com',NULL,'2023-06-19 04:08:10'),(3,'Ron','male',24,54,'df','No','ron@gmail.com',NULL,'2023-06-19 04:39:05'),(4,'harry','male',25,65,'vijayawada','No','harry@gmail.com',NULL,'2023-06-19 04:39:40'),(5,'eswar','male',23,70,'vijayawada','No','eswar@gmail.com','9701296465','2023-06-19 07:29:34'),(8,'anji','male',23,80,'Masjid street','No','anji@gmail.com','9701296462','2023-06-19 11:03:59');
/*!40000 ALTER TABLE `donor` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `agecheck` BEFORE INSERT ON `donor` FOR EACH ROW BEGIN
  IF NEW.age < 21 THEN
    SET NEW.age = 0;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `N_ID` int NOT NULL AUTO_INCREMENT,
  `NB_GROUP` varchar(4) DEFAULT NULL,
  `N_PACKETS` int DEFAULT NULL,
  `NF_NAME` varchar(50) DEFAULT NULL,
  `NADRESS` varchar(250) DEFAULT NULL,
  `RESULT` varchar(50) DEFAULT NULL,
  `STATUS` varchar(20) DEFAULT NULL,
  `CONTACT_ID` int DEFAULT NULL,
  PRIMARY KEY (`N_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=525 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (524,'O+',2,'b','1234mainroad',NULL,NULL,141);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reception`
--

DROP TABLE IF EXISTS `reception`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reception` (
  `E_ID` varchar(54) NOT NULL,
  `NAME` varchar(100) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `PASSWORD` varchar(100) DEFAULT NULL,
  `REGISTER_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`E_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reception`
--

LOCK TABLES `reception` WRITE;
/*!40000 ALTER TABLE `reception` DISABLE KEYS */;
INSERT INTO `reception` VALUES ('122','albus','z3191716@gmail.com','12345','2023-07-05 10:32:03');
/*!40000 ALTER TABLE `reception` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-05 16:23:52
