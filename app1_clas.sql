/*
Navicat MySQL Data Transfer

Source Server         : test1
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : record

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2017-12-04 17:20:01
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app1_login
-- ----------------------------
DROP TABLE IF EXISTS `app1_login`;
CREATE TABLE `app1_login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(32) NOT NULL,
  `passwd` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uname` (`uname`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of app1_login
-- ----------------------------
INSERT INTO `app1_login` VALUES ('1', 'admin', '123456');
INSERT INTO `app1_login` VALUES ('2', 'cc123', '1234567');


-- ----------------------------
-- Table structure for app1_clas
-- ----------------------------
DROP TABLE IF EXISTS `app1_clas`;
CREATE TABLE `app1_clas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clsName` varchar(128) NOT NULL,
  `startTime` date NOT NULL,
  `endTime` date NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clsName` (`clsName`),
  KEY `app1_clas_ea134da7` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of app1_clas
-- ----------------------------
INSERT INTO `app1_clas` VALUES ('1', 'cls1', '2016-06-17', '2016-10-17', '2');
INSERT INTO `app1_clas` VALUES ('2', 'cls2', '2017-11-01', '2018-03-17', '2');
INSERT INTO `app1_clas` VALUES ('3', 'cls3', '2017-05-08', '2017-08-20', '3');
INSERT INTO `app1_clas` VALUES ('4', 'cls4', '2017-04-01', '2017-09-30', '1');
INSERT INTO `app1_clas` VALUES ('5', 'cls5', '2017-03-01', '2017-08-01', '3');
INSERT INTO `app1_clas` VALUES ('6', 'cls6', '2017-06-01', '2017-12-04', '4');
INSERT INTO `app1_clas` VALUES ('30', 'cls7', '2018-01-05', '2018-04-05', '4');
INSERT INTO `app1_clas` VALUES ('31', 'cls8', '2017-12-30', '2018-04-30', '2');


-- ----------------------------
-- Table structure for app1_courses
-- ----------------------------
DROP TABLE IF EXISTS `app1_courses`;
CREATE TABLE `app1_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `couName` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `couName` (`couName`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of app1_courses
-- ----------------------------
INSERT INTO `app1_courses` VALUES ('6', 'C++');
INSERT INTO `app1_courses` VALUES ('1', 'java自动化');
INSERT INTO `app1_courses` VALUES ('3', 'Python自动化');
INSERT INTO `app1_courses` VALUES ('4', '安全');
INSERT INTO `app1_courses` VALUES ('2', '性能');

-- ----------------------------
-- Table structure for app1_stu
-- ----------------------------
DROP TABLE IF EXISTS `app1_stu`;
CREATE TABLE `app1_stu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `phoneNo` varchar(20) NOT NULL,
  `qqNo` varchar(15) NOT NULL,
  `tuition_total` double NOT NULL,
  `tuition_paid` double NOT NULL,
  `isRecommended` tinyint(1) NOT NULL,
  `clsType` int(11) NOT NULL,
  `clsId_id` int(11) NOT NULL,
  `couId_id` int(11) NOT NULL,
  `recommender_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=332 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of app1_stu
-- ----------------------------
INSERT INTO `app1_stu` VALUES ('1', 'jim Green', '18802296129', '774585295', '100000', '9999', '2', '1', '1', '2', null);
INSERT INTO `app1_stu` VALUES ('2', 'kate', '18295099366', '774686299', '10000', '6000', '1', '1', '2', '2', '1');
INSERT INTO `app1_stu` VALUES ('3', 'Liming', '13931933938', '774888298', '9000', '9000', '1', '2', '6', '4', '1');
INSERT INTO `app1_stu` VALUES ('4', 'cc', '15922692230', '774684299', '1000', '1000', '2', '1', '1', '2', null);
INSERT INTO `app1_stu` VALUES ('5', 'niuniu', '15822692230', '774685259', '5000', '1000', '2', '1', '2', '2', null);
INSERT INTO `app1_stu` VALUES ('7', 'monkey', '15822393360', '774888298', '2000', '2000', '1', '1', '1', '2', '5');
INSERT INTO `app1_stu` VALUES ('8', 'lily', '15822682280', '773683293', '7000', '6000', '2', '1', '3', '3', null);
INSERT INTO `app1_stu` VALUES ('9', 'jack', '15822592280', '2453636457', '5000', '3000', '2', '2', '3', '3', null);
INSERT INTO `app1_stu` VALUES ('10', 'rose', '13931966933', '464565756767', '5000', '5000', '2', '2', '3', '3', null);
INSERT INTO `app1_stu` VALUES ('11', 'bob', '13933399339', '774686279', '6000', '5000', '2', '1', '4', '1', null);
INSERT INTO `app1_stu` VALUES ('12', 'taintian', '15933688988', '773933292', '6000', '5000', '1', '1', '2', '2', '4');