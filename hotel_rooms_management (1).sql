-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2024 at 10:05 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_rooms_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `Id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` varchar(255) NOT NULL,
  `Date` timestamp NULL DEFAULT current_timestamp(),
  `createdBy` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`Id`, `name`, `email`, `phone`, `address`, `Date`, `createdBy`) VALUES
(8, 'Evan', 'evan@seeei.com', '01726655657', 'Rajshahi', '2024-11-11 20:58:22', 1),
(10, 'DUFUF', 'sheiibhaiiisheiii@shei.com', '234', 'Raj', '2024-11-12 16:37:41', 1),
(14, 'evan', 'dsa@ss.com', '0182282882', '', '2024-11-12 20:27:36', 1);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `Id` int(11) NOT NULL,
  `reservationId` int(11) DEFAULT NULL,
  `amount` int(11) NOT NULL,
  `discount` int(11) NOT NULL,
  `paymentDate` date NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`Id`, `reservationId`, `amount`, `discount`, `paymentDate`, `status`) VALUES
(5, 61, 455, 30, '2024-11-13', 'fss');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `Id` int(11) NOT NULL,
  `roomId` int(11) DEFAULT NULL,
  `customerId` int(11) DEFAULT NULL,
  `checkIn` date NOT NULL,
  `checkOut` date NOT NULL,
  `status` varchar(50) NOT NULL,
  `totalAmount` int(11) NOT NULL,
  `createdBy` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`Id`, `roomId`, `customerId`, `checkIn`, `checkOut`, `status`, `totalAmount`, `createdBy`) VALUES
(59, 1, 8, '2024-11-12', '2024-11-13', 'booked', 344, NULL),
(60, 1, 8, '2024-11-12', '2024-11-15', 'booked', 1032, NULL),
(61, 1, 8, '2024-11-12', '2024-11-12', 'new', 0, NULL),
(65, 1, 8, '2024-11-12', '2024-11-13', '', 344, NULL),
(66, 1, 10, '2024-11-08', '2024-11-13', 'booked', 1720, NULL),
(67, 10, 8, '2024-11-13', '2024-11-14', 's', 344, NULL),
(69, 10, 8, '2024-11-13', '2024-11-14', 's', 344, NULL),
(70, 1, 8, '2024-11-13', '2024-11-14', 's', 344, NULL),
(71, 1, 8, '2024-11-13', '2024-11-14', 'd', 23, NULL),
(72, 1, 8, '2024-11-13', '2024-11-14', 'd', 23, NULL),
(73, 1, 8, '2024-11-13', '2024-11-14', 'dd', 23, NULL),
(74, 1, 8, '2024-11-13', '2024-11-14', 'ehhe', 23, NULL),
(75, 10, 8, '2024-11-13', '2024-11-14', 'ok', 23, NULL),
(76, 1, 8, '2024-11-13', '2024-11-14', 'ok', 344, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `Id` int(11) NOT NULL,
  `roomNo` int(11) NOT NULL,
  `type` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `createdBy` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`Id`, `roomNo`, `type`, `price`, `status`, `createdBy`) VALUES
(1, 1, 'adasj', 344, 'available', 1),
(10, 101, 'r', 23, 'available', 1),
(11, 102, 'Janina', 500, 'available', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `Id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(200) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Id`, `name`, `email`, `username`, `password`, `created_at`) VALUES
(1, 'ev', '', 'e', '$2b$12$UCPuh4L6b6MevQfIjg8Jce5ML3CtwVKKC4Qe020U.95zkrE6co1X6', '0000-00-00 00:00:00'),
(3, 'Imtiaz', '', 'imtiaz', '$2b$12$t1yjnTQr.Dz38Nx0gVhr3e54quPGcSnySvwGP/GzuV7d25qlGCvaO', '0000-00-00 00:00:00'),
(4, 'evan', '', 'ev', '$2b$12$xjSOu8ogGUZ2RrdTK0MY9uWZqFx/Ng4xbKX9vjAzbt54pZDCN3RIa', '0000-00-00 00:00:00'),
(11, 'evan', 'sfs', 'dds', '$2b$12$LyQnD978TxDjDlz.kGR60.kzy1Kp4iNPZd30X7SJbB94WN.gX.8xS', '2024-11-12 20:45:49'),
(12, 'evan', 'daasd@gmai.com', 'ee', '$2b$12$iXHRKVsre2KYbVMIgxbEX.mfgAM/qC4WUILTZ9Bs4RVICwOIdtHDe', '2024-11-12 20:53:46'),
(13, 'evan', '1@d.com', '1', '$2b$12$j1oKy9PfLBCT./k2mH0pfOKva1Jdj6RfeoOEv2AAiErdvzxd3OePO', '2024-11-12 20:54:22'),
(14, 'Imtiii', 'imti@apu.com', 'imti', '$2b$12$WAwu/LBSNE8aUvcVfXAUneEbKSgYovRF3EYoSZ34tlaoeSvpqxcEK', '2024-11-12 20:58:34');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `createdBy` (`createdBy`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `reservationId` (`reservationId`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `roomId` (`roomId`),
  ADD KEY `customerId` (`customerId`),
  ADD KEY `createdBy` (`createdBy`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `roomNo` (`roomNo`),
  ADD KEY `createdBy` (`createdBy`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customers`
--
ALTER TABLE `customers`
  ADD CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`createdBy`) REFERENCES `users` (`Id`);

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`reservationId`) REFERENCES `reservations` (`Id`);

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`roomId`) REFERENCES `rooms` (`Id`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`customerId`) REFERENCES `customers` (`Id`),
  ADD CONSTRAINT `reservations_ibfk_3` FOREIGN KEY (`createdBy`) REFERENCES `users` (`Id`);

--
-- Constraints for table `rooms`
--
ALTER TABLE `rooms`
  ADD CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`createdBy`) REFERENCES `users` (`Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
