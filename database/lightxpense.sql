-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2023 at 06:19 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lightxpense`
--

-- --------------------------------------------------------

--
-- Table structure for table `chart_data`
--

CREATE TABLE `chart_data` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `date` date DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `amount` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `chart_data`
--

INSERT INTO `chart_data` (`id`, `date`, `month`, `email`, `category`, `amount`) VALUES
(1, '2023-11-01', 11, 'john@gmail.com', 'Medical', 185),
(2, '2023-11-02', 11, 'taiyongxin@gmail.com', 'Medical', 150),
(3, '2023-11-02', 11, 'john@gmail.com', 'Medical', 120),
(4, '2023-11-05', 11, 'john@gmail.com', 'Entertainment', 150),
(5, '2023-11-05', 11, 'taiyongxin@gmail.com', 'Entertainment', 120),
(6, '2023-11-06', 11, 'taiyongxin@gmail.com', 'Fuel & Petrol', 20);

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `first_name` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `last_name` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `email` text CHARACTER SET utf32 COLLATE utf32_unicode_ci NOT NULL,
  `phone_number` int(20) NOT NULL,
  `password` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `department` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`first_name`, `last_name`, `email`, `phone_number`, `password`, `department`) VALUES
('John', 'Doe', 'john@gmail.com', 0, 'test', 'marketing'),
('Yong Xin', 'Tai', 'taiyongxin@gmail.com', 17, 'abc111', 'Sales & Marketing'),
('Admin', 'Admin', 'yenwei.lightxpense@gmail.com', 18, 'abc111@', 'ADMIN');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chart_data`
--
ALTER TABLE `chart_data`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `user_details`
--
ALTER TABLE `user_details`
  ADD PRIMARY KEY (`email`(100));

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chart_data`
--
ALTER TABLE `chart_data`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=300;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
