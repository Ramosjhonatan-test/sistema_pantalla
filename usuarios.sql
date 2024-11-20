-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-11-2024 a las 07:38:15
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistemaeducativo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('profesor','estudiante') NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `contraseña`, `rol`, `activo`, `fecha_registro`) VALUES
(4, 'adan', 'adan@gmail.com', 'scrypt:32768:8:1$xYBl8rM75Vfbt2v9$8f6957de9ff348100e67d97c70754a35c6c429cc2b00369e041cc94e4293967f9d90fe9b6ec07d3341b5b1b704fc66cf5eaf768e6811e298c21de2d6d29b71a8', 'estudiante', 1, '2024-11-20 05:10:05'),
(5, 'eva', 'eva@gmail.com', 'scrypt:32768:8:1$XILWqPpeIzUkfB7j$c8b3757cc5ddadb875b1a99ed107e396dc6797742a011c4854db64003526719f7ea5c0059a2252cabf003673a54ec284f736ce729b4103cce9e8b5492d4917bf', 'estudiante', 1, '2024-11-20 05:56:22'),
(6, 'admin', 'admin@gmail.com', 'scrypt:32768:8:1$1ZFJztdGqqCqsuMo$a11238a407aeaa547be2a4c5cb26f32d415aa76483722ad36fb049c52c152d169d41a69da46ac26db192a634d431ebd2f69ac24334124d62401a52f5dcb9233a', 'estudiante', 1, '2024-11-20 05:58:53');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
