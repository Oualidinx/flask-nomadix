-- --------------------------------------------------------
-- Hôte:                         localhost
-- Version du serveur:           11.5.2-MariaDB - mariadb.org binary distribution
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour nomadix
CREATE DATABASE IF NOT EXISTS `nomadix` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `nomadix`;

-- Listage de la structure de la table nomadix. agency
CREATE TABLE IF NOT EXISTS `agency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `reserved_places` int(11) DEFAULT NULL,
  `responsible_full_name` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `code_grp` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. bus
CREATE TABLE IF NOT EXISTS `bus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(100) DEFAULT NULL,
  `driver_full_name` varchar(100) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. config
CREATE TABLE IF NOT EXISTS `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `benefice` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. contact
CREATE TABLE IF NOT EXISTS `contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `fk_bus_id` int(11) DEFAULT NULL,
  `fk_guide_id` int(11) DEFAULT NULL,
  `fk_hotel_id` int(11) DEFAULT NULL,
  `fk_agency_id` int(11) DEFAULT NULL,
  `fk_person_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_agency_id` (`fk_agency_id`),
  KEY `fk_bus_id` (`fk_bus_id`),
  KEY `fk_guide_id` (`fk_guide_id`),
  KEY `fk_hotel_id` (`fk_hotel_id`),
  KEY `fk_person_id` (`fk_person_id`),
  CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`fk_agency_id`) REFERENCES `agency` (`id`),
  CONSTRAINT `contact_ibfk_2` FOREIGN KEY (`fk_bus_id`) REFERENCES `bus` (`id`),
  CONSTRAINT `contact_ibfk_3` FOREIGN KEY (`fk_guide_id`) REFERENCES `guide` (`id`),
  CONSTRAINT `contact_ibfk_4` FOREIGN KEY (`fk_hotel_id`) REFERENCES `hotel` (`id`),
  CONSTRAINT `contact_ibfk_5` FOREIGN KEY (`fk_person_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. entity
CREATE TABLE IF NOT EXISTS `entity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `montants` int(11) DEFAULT NULL,
  `unit` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total_amount` int(11) DEFAULT NULL,
  `fk_invoice_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_invoice_id` (`fk_invoice_id`),
  CONSTRAINT `entity_ibfk_1` FOREIGN KEY (`fk_invoice_id`) REFERENCES `invoice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. guide
CREATE TABLE IF NOT EXISTS `guide` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. hotel
CREATE TABLE IF NOT EXISTS `hotel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `star_rating` int(11) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. include
CREATE TABLE IF NOT EXISTS `include` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_voyage_id` int(11) DEFAULT NULL,
  `fk_guide_id` int(11) DEFAULT NULL,
  `fk_bus_id` int(11) DEFAULT NULL,
  `fk_hotel_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_bus_id` (`fk_bus_id`),
  KEY `fk_guide_id` (`fk_guide_id`),
  KEY `fk_voyage_id` (`fk_voyage_id`),
  KEY `fk_hotel_id` (`fk_hotel_id`),
  CONSTRAINT `include_ibfk_1` FOREIGN KEY (`fk_bus_id`) REFERENCES `bus` (`id`),
  CONSTRAINT `include_ibfk_2` FOREIGN KEY (`fk_guide_id`) REFERENCES `guide` (`id`),
  CONSTRAINT `include_ibfk_3` FOREIGN KEY (`fk_voyage_id`) REFERENCES `voyage` (`id`),
  CONSTRAINT `include_ibfk_4` FOREIGN KEY (`fk_hotel_id`) REFERENCES `hotel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. invoice
CREATE TABLE IF NOT EXISTS `invoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `fk_agency_id` int(11) DEFAULT NULL,
  `invoice_type` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_agency_id` (`fk_agency_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`fk_agency_id`) REFERENCES `agency` (`id`),
  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. payment
CREATE TABLE IF NOT EXISTS `payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `fk_invoice_id` int(11) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_invoice_id` (`fk_invoice_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`fk_invoice_id`) REFERENCES `invoice` (`id`),
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. person
CREATE TABLE IF NOT EXISTS `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `fk_agency_id` int(11) DEFAULT NULL,
  `sexe` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_agency_id` (`fk_agency_id`),
  CONSTRAINT `person_ibfk_1` FOREIGN KEY (`fk_agency_id`) REFERENCES `agency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `password_hasChanged` tinyint(1) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `password_hash` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.
INSERT INTO `user` (`first_name`, `last_name`, `role`, `is_deleted`, `password_hasChanged`, `username`, `phone_number`, `password_hash`) VALUES

	('Drici', 'Abde krim', 'master', 0, 0, 'DdahCaXTcQE', 'champ vide', 'scrypt:32768:8:1$SbxVpxCCG6YL9tns$6012b0f9fb61825bddfa92b5890f3d95be6db3e7f33de4ddf70aa811a59e39fc39008414ed7da2e02993f7ceaea13351ee6b4e2a5859b1ca760c5e3611567d0d');

-- Listage de la structure de la table nomadix. voyage
CREATE TABLE IF NOT EXISTS `voyage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `destination` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `date_depart` datetime DEFAULT NULL,
  `date_end` datetime DEFAULT NULL,
  `hotel_fees` int(11) DEFAULT NULL,
  `bus_fees` int(11) DEFAULT NULL,
  `visa_fees` int(11) DEFAULT NULL,
  `guide_fees` int(11) DEFAULT NULL,
  `is_plane_included` tinyint(1) DEFAULT NULL,
  `is_guide_included` tinyint(1) DEFAULT NULL,
  `is_hotel_included` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `is_bus_included` tinyint(1) DEFAULT NULL,
  `is_visa_included` tinyint(1) DEFAULT NULL,
  `plane_fees` int(11) DEFAULT NULL,
  `subscription_due_date` datetime DEFAULT NULL,
  `nb_places` int(11) DEFAULT NULL,
  `nb_free_places` int(11) DEFAULT NULL,
  `is_submitted_for_payment` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `voyage_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table nomadix. voyage_agency
CREATE TABLE IF NOT EXISTS `voyage_agency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_agency_id` int(11) DEFAULT NULL,
  `fk_voyage_id` int(11) DEFAULT NULL,
  `total_paid` int(11) DEFAULT NULL,
  `rest_to_pay` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_agency_id` (`fk_agency_id`),
  KEY `fk_voyage_id` (`fk_voyage_id`),
  CONSTRAINT `voyage_agency_ibfk_1` FOREIGN KEY (`fk_agency_id`) REFERENCES `agency` (`id`),
  CONSTRAINT `voyage_agency_ibfk_2` FOREIGN KEY (`fk_voyage_id`) REFERENCES `voyage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Les données exportées n'étaient pas sélectionnées.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
