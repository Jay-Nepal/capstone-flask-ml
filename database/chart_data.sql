/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `chart_data`;
CREATE TABLE `chart_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `dept` varchar(255) DEFAULT NULL,
  `status_invoice` varchar(255) DEFAULT NULL,
  `po_amount` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=300 DEFAULT CHARSET=latin1;

INSERT INTO `chart_data` (`id`, `date`, `month`, `dept`, `status_invoice`, `po_amount`) VALUES
(1, '2021-06-01', 6, 'D021', 'Completely', 18650);
INSERT INTO `chart_data` (`id`, `date`, `month`, `dept`, `status_invoice`, `po_amount`) VALUES
(2, '2021-06-01', 6, 'D015', 'Completely', 15000);
INSERT INTO `chart_data` (`id`, `date`, `month`, `dept`, `status_invoice`, `po_amount`) VALUES
(3, '2021-06-01', 6, 'D046', 'Partly', 15120);
INSERT INTO `chart_data` (`id`, `date`, `month`, `dept`, `status_invoice`, `po_amount`) VALUES
(4, '2021-06-01', 6, 'D068', 'No', 12320),
(5, '2021-06-02', 6, 'D017', 'Completely', 18056),
(6, '2021-06-02', 6, 'D017', 'No', 802),
(7, '2021-06-03', 6, 'D016', 'No', 17568.5),
(8, '2021-06-03', 6, 'D017', 'Completely', 1435),
(9, '2021-06-03', 6, 'D017', 'No', 15864),
(10, '2021-06-03', 6, 'D023', 'No', 654404),
(11, '2021-06-03', 6, 'D025', 'Completely', 192),
(12, '2021-06-04', 6, 'D017', 'Completely', 31379.3),
(13, '2021-06-04', 6, 'D017', 'No', 84375),
(14, '2021-06-04', 6, 'D025', 'Partly', 9000),
(15, '2021-06-08', 6, 'D017', 'Completely', 101781),
(16, '2021-06-08', 6, 'D025', 'Completely', 1050),
(17, '2021-06-08', 6, 'D022', 'Completely', 2170),
(18, '2021-06-08', 6, 'D062', 'No', 5779.2),
(19, '2021-06-09', 6, 'D016', 'No', 982),
(20, '2021-06-09', 6, 'D017', 'Completely', 63500),
(21, '2021-06-09', 6, 'D017', 'No', 39582.5),
(22, '2021-06-09', 6, 'D046', 'Completely', 791732),
(23, '2021-06-10', 6, 'D017', 'Completely', 432438),
(24, '2021-06-10', 6, 'D017', 'No', 7916.8),
(25, '2021-06-10', 6, 'D020', 'No', 10800),
(26, '2021-06-10', 6, 'D020', 'Partly', 8050),
(27, '2021-06-10', 6, 'D021', 'Completely', 119954),
(28, '2021-06-10', 6, 'D021', 'No', 22970),
(29, '2021-06-10', 6, 'D042', 'No', 185000),
(30, '2021-06-10', 6, 'D008', 'No', 133102),
(31, '2021-06-11', 6, 'D016', 'Completely', 86461),
(32, '2021-06-11', 6, 'D017', 'Completely', 1553100),
(33, '2021-06-11', 6, 'D017', 'No', 7845.56),
(34, '2021-06-11', 6, 'D017', 'Partly', 5850),
(35, '2021-06-14', 6, 'D017', 'No', 6910),
(36, '2021-06-14', 6, 'D025', 'Completely', 21396),
(37, '2021-06-14', 6, 'D015', 'Completely', 4200),
(38, '2021-06-14', 6, 'D046', 'No', 600),
(39, '2021-06-15', 6, 'D016', 'No', 5202.63),
(40, '2021-06-15', 6, 'D017', 'Completely', 1153990),
(41, '2021-06-15', 6, 'D017', 'No', 9020),
(42, '2021-06-15', 6, 'D017', 'Partly', 3372910),
(43, '2021-06-16', 6, 'D017', 'Completely', 1220),
(44, '2021-06-16', 6, 'D017', 'No', 11383.3),
(45, '2021-06-16', 6, 'D022', 'Partly', 1248760),
(46, '2021-06-17', 6, 'D016', 'No', 1150),
(47, '2021-06-17', 6, 'D022', 'Completely', 597.5),
(48, '2021-06-18', 6, 'D017', 'No', 36496),
(49, '2021-06-18', 6, 'D025', 'Completely', 676.27),
(50, '2021-06-21', 6, 'D017', 'Completely', 9643),
(51, '2021-06-21', 6, 'D017', 'No', 37061),
(52, '2021-06-21', 6, 'D015', 'Completely', 4200),
(53, '2021-06-21', 6, 'D015', 'No', 7800),
(54, '2021-06-21', 6, 'D022', 'Completely', 500),
(55, '2021-06-22', 6, 'D017', 'Completely', 7000),
(56, '2021-06-22', 6, 'D021', 'No', 8519.84),
(57, '2021-06-22', 6, 'D025', 'Partly', 38994.7),
(58, '2021-06-23', 6, 'D017', 'Completely', 1386190),
(59, '2021-06-23', 6, 'D017', 'No', 196587),
(60, '2021-06-23', 6, 'D017', 'Partly', 59119.9),
(61, '2021-06-23', 6, 'D021', 'Partly', 12070),
(62, '2021-06-23', 6, 'D025', 'Completely', 798.73),
(63, '2021-06-24', 6, 'D017', 'Completely', 292),
(64, '2021-06-24', 6, 'D017', 'No', 1200),
(65, '2021-06-24', 6, 'D025', 'Completely', 108702),
(66, '2021-06-24', 6, 'D043', 'No', 110590),
(67, '2021-06-24', 6, 'D046', 'No', 710),
(68, '2021-06-25', 6, 'D017', 'Completely', 22230.8),
(69, '2021-06-25', 6, 'D017', 'No', 51467.4),
(70, '2021-06-25', 6, 'D021', 'Completely', 10000),
(71, '2021-06-25', 6, 'D025', 'Completely', 6390),
(72, '2021-06-25', 6, 'D025', 'No', 118231),
(73, '2021-06-25', 6, 'D022', 'No', 1890),
(74, '2021-06-25', 6, 'D068', 'No', 9280),
(75, '2021-06-27', 6, 'D043', 'Completely', 380),
(76, '2021-06-28', 6, 'D017', 'Completely', 626324),
(77, '2021-06-28', 6, 'D017', 'No', 2015),
(78, '2021-06-28', 6, 'D017', 'Partly', 177600),
(79, '2021-06-28', 6, 'D023', 'Completely', 4114),
(80, '2021-06-29', 6, 'D017', 'No', 18850),
(81, '2021-06-29', 6, 'D023', 'No', 220901),
(82, '2021-06-30', 6, 'D016', 'No', 450),
(83, '2021-06-30', 6, 'D017', 'Completely', 399.87),
(84, '2021-06-30', 6, 'D017', 'No', 1162.45),
(85, '2021-06-30', 6, 'D021', 'Completely', 8820),
(86, '2021-06-30', 6, 'D021', 'No', 650),
(87, '2021-06-30', 6, 'D023', 'Completely', 28259),
(88, '2021-06-30', 6, 'D025', 'Completely', 46394.2),
(89, '2021-06-30', 6, 'D043', 'No', 53835),
(90, '2021-06-30', 6, 'D046', 'No', 8395.73),
(91, '2021-06-30', 6, NULL, 'No', 25700),
(92, '2021-07-01', 7, 'D017', 'Completely', 11640),
(93, '2021-07-01', 7, 'D017', 'No', 8750),
(94, '2021-07-01', 7, 'D023', 'No', 29500),
(95, '2021-07-02', 7, 'D017', 'Completely', 31140),
(96, '2021-07-02', 7, 'D017', 'No', 241380),
(97, '2021-07-05', 7, 'D017', 'No', 595153),
(98, '2021-07-05', 7, 'D017', 'Partly', 508030),
(99, '2021-07-06', 7, 'D017', 'Completely', 46990),
(100, '2021-07-06', 7, 'D017', 'No', 390),
(101, '2021-07-06', 7, 'D017', 'Partly', 12600),
(102, '2021-07-07', 7, 'D017', 'No', 7425.68),
(103, '2021-07-08', 7, 'D017', 'Completely', 1000),
(104, '2021-07-08', 7, 'D023', 'Completely', 750),
(105, '2021-07-08', 7, 'D023', 'No', 61799),
(106, '2021-07-09', 7, 'D017', 'Completely', 47200),
(107, '2021-07-09', 7, 'D017', 'No', 1103.2),
(108, '2021-07-09', 7, 'D021', 'Completely', 7550),
(109, '2021-07-12', 7, 'D017', 'Completely', 2710.7),
(110, '2021-07-12', 7, 'D017', 'No', 1830),
(111, '2021-07-12', 7, 'D025', 'No', 1000),
(112, '2021-07-12', 7, 'D015', 'No', 7800),
(113, '2021-07-12', 7, 'D046', 'No', 5695),
(114, '2021-07-13', 7, 'D017', 'Completely', 700),
(115, '2021-07-13', 7, 'D017', 'No', 33670),
(116, '2021-07-14', 7, 'D016', 'Completely', 5990),
(117, '2021-07-14', 7, 'D017', 'Completely', 27235),
(118, '2021-07-14', 7, 'D017', 'No', 45728),
(119, '2021-07-14', 7, 'D043', 'No', 1275),
(120, '2021-07-16', 7, 'D017', 'No', 628.5),
(121, '2021-07-16', 7, 'D022', 'No', 8138),
(122, '2021-07-18', 7, 'D016', 'Completely', 2186.64),
(123, '2021-07-18', 7, 'D016', 'No', 1425),
(124, '2021-07-19', 7, 'D016', 'No', 2445),
(125, '2021-07-19', 7, 'D017', 'Completely', 461796),
(126, '2021-07-19', 7, 'D017', 'No', 21500),
(127, '2021-07-19', 7, 'D017', 'Partly', 104130),
(128, '2021-07-19', 7, 'D021', 'Partly', 13580),
(129, '2021-07-19', 7, 'D022', 'No', 94720),
(130, '2021-07-19', 7, 'D043', 'No', 239720),
(131, '2021-07-19', 7, 'D046', 'Completely', 870),
(132, '2021-07-21', 7, 'D017', 'No', 7604.85),
(133, '2021-07-21', 7, 'D025', 'No', 1350),
(134, '2021-07-22', 7, 'D017', 'No', 1200),
(135, '2021-07-24', 7, 'D017', 'No', 4655),
(136, '2021-07-26', 7, 'D017', 'Completely', 51200.6),
(137, '2021-07-26', 7, 'D017', 'No', 9648),
(138, '2021-07-26', 7, 'D020', 'Completely', 7740),
(139, '2021-07-26', 7, 'D020', 'No', 36000),
(140, '2021-07-26', 7, 'D021', 'Completely', 186726),
(141, '2021-07-26', 7, 'D021', 'No', 216746),
(142, '2021-07-26', 7, 'D023', 'No', 21287),
(143, '2021-07-26', 7, 'D025', 'No', 31740),
(144, '2021-07-26', 7, 'D022', 'No', 1863.5),
(145, '2021-07-26', 7, 'D046', 'No', 20980.2),
(146, '2021-07-27', 7, 'D017', 'No', 570463),
(147, '2021-07-29', 7, 'D017', 'Completely', 3448),
(148, '2021-07-29', 7, 'D017', 'No', 25295.2),
(149, '2021-07-29', 7, 'D017', 'Partly', 2168),
(150, '2021-07-29', 7, 'D021', 'No', 5500),
(151, '2021-07-29', 7, 'D023', 'Completely', 507.03),
(152, '2021-07-29', 7, 'D023', 'No', 245924),
(153, '2021-07-29', 7, 'D040', 'Completely', 8560),
(154, '2021-07-30', 7, 'D016', 'Completely', 1788),
(155, '2021-07-30', 7, 'D016', 'No', 1910),
(156, '2021-07-30', 7, 'D017', 'No', 6300),
(157, '2021-07-31', 7, 'D016', 'No', 1368),
(158, '2021-08-02', 8, 'D017', 'No', 7740),
(159, '2021-08-02', 8, 'D021', 'Completely', 17818),
(160, '2021-08-02', 8, 'D043', 'Partly', 70800),
(161, '2021-08-03', 8, 'D017', 'No', 3020.68),
(162, '2021-08-04', 8, 'D017', 'Completely', 600),
(163, '2021-08-04', 8, 'D017', 'No', 5959.49),
(164, '2021-08-04', 8, 'D020', 'No', 2134),
(165, '2021-08-04', 8, 'D021', 'Completely', 577.31),
(166, '2021-08-04', 8, 'D021', 'No', 3096),
(167, '2021-08-04', 8, 'D043', 'No', 2100),
(168, '2021-08-05', 8, 'D021', 'No', 22600),
(169, '2021-08-05', 8, 'D043', 'Partly', 358674),
(170, '2021-08-05', 8, 'D040', 'No', 2361100),
(171, '2021-08-08', 8, 'D016', 'Completely', 1867),
(172, '2021-08-09', 8, 'D016', 'No', 9501),
(173, '2021-08-09', 8, 'D015', 'No', 3001.39),
(174, '2021-08-11', 8, 'D017', 'Completely', 17746),
(175, '2021-08-11', 8, 'D017', 'No', 30914),
(176, '2021-08-11', 8, 'D017', 'Partly', 25000),
(177, '2021-08-11', 8, 'D021', 'No', 11160),
(178, '2021-08-11', 8, 'D043', 'No', 58776),
(179, '2021-08-12', 8, 'D017', 'No', 10500),
(180, '2021-08-12', 8, 'D022', 'No', 3940),
(181, '2021-08-12', 8, 'D043', 'No', 25276),
(182, '2021-08-13', 8, 'D017', 'Completely', 46200),
(183, '2021-08-13', 8, 'D017', 'No', 41972.5),
(184, '2021-08-13', 8, 'D025', 'No', 780),
(185, '2021-08-13', 8, 'D043', 'No', 329661),
(186, '2021-08-13', 8, 'D046', 'No', 1010),
(187, '2021-08-14', 8, 'D043', 'No', 784093),
(188, '2021-08-16', 8, 'D017', 'Completely', 2000),
(189, '2021-08-16', 8, 'D017', 'No', 19920),
(190, '2021-08-16', 8, 'D021', 'Completely', 286558),
(191, '2021-08-16', 8, 'D021', 'No', 42710),
(192, '2021-08-16', 8, 'D023', 'No', 9500.5),
(193, '2021-08-16', 8, 'D023', 'Partly', 43200),
(194, '2021-08-16', 8, 'D043', 'Completely', 42274),
(195, '2021-08-16', 8, 'D043', 'No', 28128),
(196, '2021-08-16', 8, 'D046', 'No', 10456),
(197, '2021-08-17', 8, 'D017', 'No', 320),
(198, '2021-08-17', 8, 'D021', 'Completely', 9724),
(199, '2021-08-17', 8, 'D021', 'No', 23200),
(200, '2021-08-18', 8, 'D017', 'Completely', 15129.5),
(201, '2021-08-18', 8, 'D017', 'No', 27198.7),
(202, '2021-08-18', 8, 'D017', 'Partly', 2520),
(203, '2021-08-18', 8, 'D025', 'No', 127558),
(204, '2021-08-18', 8, 'D071', 'Completely', 821576),
(205, '2021-08-19', 8, 'D017', 'Completely', 638.6),
(206, '2021-08-19', 8, 'D017', 'No', 15315.6),
(207, '2021-08-20', 8, 'D016', 'No', 1790),
(208, '2021-08-20', 8, 'D025', 'No', 4382),
(209, '2021-08-20', 8, 'D043', 'No', 14525),
(210, '2021-08-22', 8, 'D016', 'No', 1061.69),
(211, '2021-08-23', 8, 'D016', 'No', 5400),
(212, '2021-08-23', 8, 'D017', 'Completely', 8474.8),
(213, '2021-08-24', 8, 'D017', 'No', 57076.4),
(214, '2021-08-24', 8, 'D017', 'Partly', 29200),
(215, '2021-08-24', 8, 'D021', 'Completely', 90530),
(216, '2021-08-24', 8, 'D021', 'No', 234130),
(217, '2021-08-25', 8, 'D017', 'No', 20043.5),
(218, '2021-08-25', 8, 'D015', 'Completely', 7800),
(219, '2021-08-25', 8, 'D015', 'No', 2092.9),
(220, '2021-08-25', 8, 'D043', 'No', 18623),
(221, '2021-08-26', 8, 'D017', 'Completely', 2666.86),
(222, '2021-08-26', 8, 'D017', 'No', 7400.42),
(223, '2021-08-26', 8, 'D017', 'Partly', 13655.8),
(224, '2021-08-26', 8, 'D021', 'No', 14830),
(225, '2021-08-26', 8, 'D023', 'Completely', 2250),
(226, '2021-08-26', 8, 'D023', 'No', 74012),
(227, '2021-08-26', 8, 'D046', 'No', 52248),
(228, '2021-08-27', 8, 'D017', 'Completely', 10111.8),
(229, '2021-08-27', 8, 'D017', 'No', 88545),
(230, '2021-08-27', 8, 'D021', 'No', 7200),
(231, '2021-08-27', 8, 'D025', 'Completely', 554.63),
(232, '2021-08-29', 8, 'D046', 'Partly', 4600),
(233, '2021-08-30', 8, 'D021', 'No', 41400),
(234, '2021-08-30', 8, 'D023', 'Partly', 2479520),
(235, '2021-08-31', 8, 'D043', 'No', 250),
(236, '2021-08-31', 8, 'D046', 'No', 800),
(237, '2021-09-01', 9, 'D017', 'Completely', 11650),
(238, '2021-09-01', 9, 'D017', 'No', 30339.9),
(239, '2021-09-01', 9, 'D017', 'Partly', 3810),
(240, '2021-09-01', 9, 'D021', 'Completely', 524541),
(241, '2021-09-02', 9, 'D016', 'No', 5735.9),
(242, '2021-09-02', 9, 'D043', 'No', 101250),
(243, '2021-09-02', 9, 'D046', 'No', 14300),
(244, '2021-09-03', 9, 'D017', 'No', 9660),
(245, '2021-09-03', 9, 'D021', 'Completely', 23480),
(246, '2021-09-03', 9, 'D021', 'No', 34350),
(247, '2021-09-03', 9, 'D043', 'Completely', 1368),
(248, '2021-09-03', 9, 'D043', 'No', 164782),
(249, '2021-09-05', 9, 'D016', 'No', 16063.1),
(250, '2021-09-06', 9, 'D016', 'No', 27993.4),
(251, '2021-09-06', 9, 'D017', 'No', 55080),
(252, '2021-09-06', 9, 'D021', 'Completely', 495.98),
(253, '2021-09-06', 9, 'D023', 'No', 195596),
(254, '2021-09-06', 9, 'D025', 'No', 154919),
(255, '2021-09-07', 9, 'D017', 'Completely', 5000),
(256, '2021-09-07', 9, 'D017', 'No', 47162.6),
(257, '2021-09-07', 9, 'D015', 'Completely', 8400),
(258, '2021-09-07', 9, 'D043', 'Completely', 1580),
(259, '2021-09-08', 9, 'D021', 'Completely', 118048),
(260, '2021-09-08', 9, 'D021', 'No', 640),
(261, '2021-09-08', 9, 'D043', 'No', 59029.7),
(262, '2021-09-09', 9, 'D017', 'No', 22619.7),
(263, '2021-09-09', 9, 'D021', 'Completely', 16500),
(264, '2021-09-09', 9, 'D015', 'No', 3432),
(265, '2021-09-09', 9, 'D043', 'Completely', 4750),
(266, '2021-09-09', 9, 'D043', 'No', 6743.5),
(267, '2021-09-13', 9, 'D021', 'Completely', 888228),
(268, '2021-09-13', 9, 'D021', 'No', 12412.4),
(269, '2021-09-13', 9, 'D023', 'No', 533690),
(270, '2021-09-13', 9, 'D025', 'Partly', 3014.5),
(271, '2021-09-15', 9, 'D016', 'No', 19600),
(272, '2021-09-15', 9, 'D017', 'No', 31559.5),
(273, '2021-09-16', 9, 'D017', 'No', 5500),
(274, '2021-09-17', 9, 'D017', 'No', 77889),
(275, '2021-09-17', 9, 'D023', 'No', 17738),
(276, '2021-09-17', 9, 'D015', 'No', 8475),
(277, '2021-09-17', 9, 'D043', 'No', 340),
(278, '2021-09-20', 9, 'D016', 'No', 1181.6),
(279, '2021-09-20', 9, 'D017', 'No', 432289),
(280, '2021-09-20', 9, 'D021', 'Completely', 5510),
(281, '2021-09-20', 9, 'D021', 'No', 40183.8),
(282, '2021-09-20', 9, 'D025', 'No', 350),
(283, '2021-09-20', 9, 'D043', 'No', 322461),
(284, '2021-09-20', 9, 'D046', 'No', 8816),
(285, '2021-09-21', 9, 'D016', 'No', 1020),
(286, '2021-09-21', 9, 'D017', 'No', 20475),
(287, '2021-09-21', 9, 'D025', 'No', 39723.1),
(288, '2021-09-21', 9, 'D015', 'No', 7496),
(289, '2021-09-22', 9, 'D017', 'No', 48673.7),
(290, '2021-09-22', 9, 'D021', 'No', 1339.32),
(291, '2021-09-22', 9, 'D025', 'No', 4062),
(292, '2021-09-23', 9, 'D017', 'Completely', 35548.4),
(293, '2021-09-23', 9, 'D017', 'No', 37500),
(294, '2021-09-23', 9, 'D043', 'No', 730),
(295, '2021-09-24', 9, 'D017', 'No', 10836),
(296, '2021-09-24', 9, 'D020', 'No', 14542),
(297, '2021-09-24', 9, 'D021', 'No', 111515),
(298, '2021-09-24', 9, 'D023', 'No', 51808),
(299, '2021-09-24', 9, 'D046', 'No', 1680);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;