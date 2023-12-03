-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2022 at 04:39 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `squarewo_sunway`
--

-- --------------------------------------------------------

--
-- Table structure for table `data_entry`
--

CREATE TABLE `data_entry` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `description` text NOT NULL,
  `quantity` int(10) NOT NULL,
  `price` double NOT NULL,
  `created_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_entry`
--

INSERT INTO `data_entry` (`id`, `category`, `description`, `quantity`, `price`, `created_date`) VALUES
(1, '', '', 0, 0, '2022-05-07 06:54:35'),
(2, '2', 'hjdjfhfkgkadshkghjasg', 2000, 25, '2022-05-11 06:34:16'),
(3, '1', 'product A', 0, 700, '2022-05-17 14:15:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `data_entry`
--
ALTER TABLE `data_entry`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `data_entry`
--
ALTER TABLE `data_entry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
