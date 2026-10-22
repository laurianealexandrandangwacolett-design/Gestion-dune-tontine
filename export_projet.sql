BEGIN TRANSACTION;
CREATE TABLE administrateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    empreinte TEXT NOT NULL
);
INSERT INTO "administrateurs" VALUES(1,'admin','scrypt:32768:8:1$Jb6bvAlLzHKro89E$62c7aabb2281331f06939be8c8810584d30f8b11e0fb36d946f8e642ea074486319c5fe4eaf459f6f96f4f02ba4a73692c68541b3e0a6c35ff419fbde52cc09a');
CREATE TABLE cotisations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seance_id INTEGER NOT NULL REFERENCES seances(id) ON DELETE CASCADE,
    membre_id INTEGER NOT NULL REFERENCES membres(id),
    montant INTEGER NOT NULL CHECK (montant > 0),
    date_paiement TEXT NOT NULL,
    mode TEXT NOT NULL CHECK (mode IN ('especes', 'mobile_money')),
    UNIQUE (seance_id, membre_id)
);
INSERT INTO "cotisations" VALUES(1,1,1,10000,'2026-07-30','especes');
INSERT INTO "cotisations" VALUES(2,1,2,10000,'2026-07-30','especes');
INSERT INTO "cotisations" VALUES(3,1,3,10000,'2026-07-31','especes');
INSERT INTO "cotisations" VALUES(4,1,4,10000,'2026-07-31','mobile_money');
INSERT INTO "cotisations" VALUES(5,1,5,10000,'2026-07-31','mobile_money');
INSERT INTO "cotisations" VALUES(6,1,6,10000,'2026-07-30','especes');
INSERT INTO "cotisations" VALUES(7,1,7,10000,'2026-07-31','especes');
INSERT INTO "cotisations" VALUES(8,1,8,10000,'2026-08-01','especes');
INSERT INTO "cotisations" VALUES(9,1,9,10000,'2026-07-30','mobile_money');
INSERT INTO "cotisations" VALUES(10,1,10,10000,'2026-08-01','mobile_money');
INSERT INTO "cotisations" VALUES(11,1,11,10000,'2026-08-01','mobile_money');
INSERT INTO "cotisations" VALUES(12,1,12,10000,'2026-07-30','mobile_money');
INSERT INTO "cotisations" VALUES(13,1,13,10000,'2026-07-30','mobile_money');
INSERT INTO "cotisations" VALUES(14,1,14,10000,'2026-08-02','especes');
INSERT INTO "cotisations" VALUES(15,1,15,10000,'2026-07-31','especes');
INSERT INTO "cotisations" VALUES(16,1,16,10000,'2026-08-01','mobile_money');
INSERT INTO "cotisations" VALUES(17,1,17,10000,'2026-07-30','mobile_money');
INSERT INTO "cotisations" VALUES(18,1,19,10000,'2026-07-30','mobile_money');
INSERT INTO "cotisations" VALUES(19,1,20,10000,'2026-08-01','mobile_money');
INSERT INTO "cotisations" VALUES(20,1,21,10000,'2026-07-30','mobile_money');
INSERT INTO "cotisations" VALUES(21,1,22,10000,'2026-08-01','mobile_money');
INSERT INTO "cotisations" VALUES(22,1,23,10000,'2026-08-04','mobile_money');
INSERT INTO "cotisations" VALUES(23,1,25,10000,'2026-08-01','mobile_money');
INSERT INTO "cotisations" VALUES(24,2,1,10000,'2026-08-10','mobile_money');
INSERT INTO "cotisations" VALUES(25,2,2,10000,'2026-08-14','especes');
INSERT INTO "cotisations" VALUES(26,2,4,10000,'2026-08-08','mobile_money');
INSERT INTO "cotisations" VALUES(27,2,5,10000,'2026-08-06','especes');
INSERT INTO "cotisations" VALUES(28,2,6,10000,'2026-08-08','especes');
INSERT INTO "cotisations" VALUES(29,2,7,10000,'2026-08-08','mobile_money');
INSERT INTO "cotisations" VALUES(30,2,8,10000,'2026-08-06','mobile_money');
INSERT INTO "cotisations" VALUES(31,2,9,10000,'2026-08-06','especes');
INSERT INTO "cotisations" VALUES(32,2,10,10000,'2026-08-07','mobile_money');
INSERT INTO "cotisations" VALUES(33,2,11,10000,'2026-08-07','mobile_money');
INSERT INTO "cotisations" VALUES(34,2,12,10000,'2026-08-09','especes');
INSERT INTO "cotisations" VALUES(35,2,13,10000,'2026-08-06','mobile_money');
INSERT INTO "cotisations" VALUES(36,2,14,10000,'2026-08-08','mobile_money');
INSERT INTO "cotisations" VALUES(37,2,15,10000,'2026-08-08','mobile_money');
INSERT INTO "cotisations" VALUES(38,2,16,10000,'2026-08-09','mobile_money');
INSERT INTO "cotisations" VALUES(39,2,17,10000,'2026-08-06','especes');
INSERT INTO "cotisations" VALUES(40,2,18,10000,'2026-08-10','mobile_money');
INSERT INTO "cotisations" VALUES(41,2,19,10000,'2026-08-10','mobile_money');
INSERT INTO "cotisations" VALUES(42,2,21,10000,'2026-08-06','especes');
INSERT INTO "cotisations" VALUES(43,2,22,10000,'2026-08-08','mobile_money');
INSERT INTO "cotisations" VALUES(44,2,23,10000,'2026-08-06','especes');
INSERT INTO "cotisations" VALUES(45,2,24,10000,'2026-08-08','especes');
INSERT INTO "cotisations" VALUES(46,2,25,10000,'2026-08-13','mobile_money');
INSERT INTO "cotisations" VALUES(47,3,2,10000,'2026-08-13','mobile_money');
INSERT INTO "cotisations" VALUES(48,3,3,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(49,3,4,10000,'2026-08-14','mobile_money');
INSERT INTO "cotisations" VALUES(50,3,5,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(51,3,6,10000,'2026-08-14','mobile_money');
INSERT INTO "cotisations" VALUES(52,3,7,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(53,3,8,10000,'2026-08-16','mobile_money');
INSERT INTO "cotisations" VALUES(54,3,9,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(55,3,10,10000,'2026-08-13','especes');
INSERT INTO "cotisations" VALUES(56,3,11,10000,'2026-08-21','especes');
INSERT INTO "cotisations" VALUES(57,3,12,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(58,3,13,10000,'2026-08-13','mobile_money');
INSERT INTO "cotisations" VALUES(59,3,14,10000,'2026-08-13','mobile_money');
INSERT INTO "cotisations" VALUES(60,3,15,10000,'2026-08-14','especes');
INSERT INTO "cotisations" VALUES(61,3,16,10000,'2026-08-16','mobile_money');
INSERT INTO "cotisations" VALUES(62,3,17,10000,'2026-08-14','mobile_money');
INSERT INTO "cotisations" VALUES(63,3,18,10000,'2026-08-13','mobile_money');
INSERT INTO "cotisations" VALUES(64,3,19,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(65,3,20,10000,'2026-08-17','especes');
INSERT INTO "cotisations" VALUES(66,3,21,10000,'2026-08-15','mobile_money');
INSERT INTO "cotisations" VALUES(67,3,22,10000,'2026-08-16','mobile_money');
INSERT INTO "cotisations" VALUES(68,3,23,10000,'2026-08-14','especes');
INSERT INTO "cotisations" VALUES(69,3,24,10000,'2026-08-17','mobile_money');
INSERT INTO "cotisations" VALUES(70,3,25,10000,'2026-08-16','mobile_money');
INSERT INTO "cotisations" VALUES(71,4,1,10000,'2026-08-28','especes');
INSERT INTO "cotisations" VALUES(72,4,2,10000,'2026-08-22','mobile_money');
INSERT INTO "cotisations" VALUES(73,4,4,10000,'2026-08-26','mobile_money');
INSERT INTO "cotisations" VALUES(74,4,5,10000,'2026-08-22','mobile_money');
INSERT INTO "cotisations" VALUES(75,4,6,10000,'2026-08-25','mobile_money');
INSERT INTO "cotisations" VALUES(76,4,7,10000,'2026-08-27','mobile_money');
INSERT INTO "cotisations" VALUES(77,4,8,10000,'2026-08-24','especes');
INSERT INTO "cotisations" VALUES(78,4,9,10000,'2026-08-21','mobile_money');
INSERT INTO "cotisations" VALUES(79,4,10,10000,'2026-08-20','especes');
INSERT INTO "cotisations" VALUES(80,4,11,10000,'2026-08-24','mobile_money');
INSERT INTO "cotisations" VALUES(81,4,12,10000,'2026-08-28','especes');
INSERT INTO "cotisations" VALUES(82,4,13,10000,'2026-08-21','mobile_money');
INSERT INTO "cotisations" VALUES(83,4,15,10000,'2026-08-22','especes');
INSERT INTO "cotisations" VALUES(84,4,16,10000,'2026-08-20','mobile_money');
INSERT INTO "cotisations" VALUES(85,4,17,10000,'2026-08-20','mobile_money');
INSERT INTO "cotisations" VALUES(86,4,18,10000,'2026-08-21','especes');
INSERT INTO "cotisations" VALUES(87,4,19,10000,'2026-08-20','mobile_money');
INSERT INTO "cotisations" VALUES(88,4,20,10000,'2026-08-25','mobile_money');
INSERT INTO "cotisations" VALUES(89,4,21,10000,'2026-08-21','mobile_money');
INSERT INTO "cotisations" VALUES(90,4,22,10000,'2026-08-20','mobile_money');
INSERT INTO "cotisations" VALUES(91,4,23,10000,'2026-08-20','especes');
INSERT INTO "cotisations" VALUES(92,4,24,10000,'2026-08-22','especes');
INSERT INTO "cotisations" VALUES(93,4,25,10000,'2026-08-24','mobile_money');
INSERT INTO "cotisations" VALUES(94,5,1,10000,'2026-08-28','mobile_money');
INSERT INTO "cotisations" VALUES(95,5,2,10000,'2026-08-27','especes');
INSERT INTO "cotisations" VALUES(96,5,3,10000,'2026-08-29','especes');
INSERT INTO "cotisations" VALUES(97,5,4,10000,'2026-08-30','mobile_money');
INSERT INTO "cotisations" VALUES(98,5,5,10000,'2026-08-27','mobile_money');
INSERT INTO "cotisations" VALUES(99,5,6,10000,'2026-08-29','mobile_money');
INSERT INTO "cotisations" VALUES(100,5,7,10000,'2026-09-03','mobile_money');
INSERT INTO "cotisations" VALUES(101,5,8,10000,'2026-08-27','especes');
INSERT INTO "cotisations" VALUES(102,5,9,10000,'2026-09-02','mobile_money');
INSERT INTO "cotisations" VALUES(103,5,10,10000,'2026-08-29','especes');
INSERT INTO "cotisations" VALUES(104,5,11,10000,'2026-08-28','especes');
INSERT INTO "cotisations" VALUES(105,5,12,10000,'2026-08-27','mobile_money');
INSERT INTO "cotisations" VALUES(106,5,13,10000,'2026-08-27','mobile_money');
INSERT INTO "cotisations" VALUES(107,5,14,10000,'2026-08-27','mobile_money');
INSERT INTO "cotisations" VALUES(108,5,15,10000,'2026-08-28','mobile_money');
INSERT INTO "cotisations" VALUES(109,5,16,10000,'2026-08-29','mobile_money');
INSERT INTO "cotisations" VALUES(110,5,17,10000,'2026-08-27','mobile_money');
INSERT INTO "cotisations" VALUES(111,5,19,10000,'2026-08-28','mobile_money');
INSERT INTO "cotisations" VALUES(112,5,20,10000,'2026-09-02','especes');
INSERT INTO "cotisations" VALUES(113,5,21,10000,'2026-08-29','mobile_money');
INSERT INTO "cotisations" VALUES(114,5,22,10000,'2026-08-29','mobile_money');
INSERT INTO "cotisations" VALUES(115,5,23,10000,'2026-08-28','especes');
INSERT INTO "cotisations" VALUES(116,5,24,10000,'2026-08-29','especes');
INSERT INTO "cotisations" VALUES(117,5,25,10000,'2026-09-03','especes');
INSERT INTO "cotisations" VALUES(118,6,1,10000,'2026-09-04','mobile_money');
INSERT INTO "cotisations" VALUES(119,6,2,10000,'2026-09-05','mobile_money');
INSERT INTO "cotisations" VALUES(120,6,3,10000,'2026-09-04','mobile_money');
INSERT INTO "cotisations" VALUES(121,6,4,10000,'2026-09-08','mobile_money');
INSERT INTO "cotisations" VALUES(122,6,5,10000,'2026-09-07','especes');
INSERT INTO "cotisations" VALUES(123,6,6,10000,'2026-09-05','mobile_money');
INSERT INTO "cotisations" VALUES(124,6,8,10000,'2026-09-05','especes');
INSERT INTO "cotisations" VALUES(125,6,10,10000,'2026-09-03','especes');
INSERT INTO "cotisations" VALUES(126,6,11,10000,'2026-09-05','mobile_money');
INSERT INTO "cotisations" VALUES(127,6,12,10000,'2026-09-04','especes');
INSERT INTO "cotisations" VALUES(128,6,13,10000,'2026-09-09','especes');
INSERT INTO "cotisations" VALUES(129,6,14,10000,'2026-09-03','mobile_money');
INSERT INTO "cotisations" VALUES(130,6,15,10000,'2026-09-05','especes');
INSERT INTO "cotisations" VALUES(131,6,16,10000,'2026-09-04','especes');
INSERT INTO "cotisations" VALUES(132,6,17,10000,'2026-09-04','mobile_money');
INSERT INTO "cotisations" VALUES(133,6,18,10000,'2026-09-06','mobile_money');
INSERT INTO "cotisations" VALUES(134,6,19,10000,'2026-09-11','mobile_money');
INSERT INTO "cotisations" VALUES(135,6,21,10000,'2026-09-04','especes');
INSERT INTO "cotisations" VALUES(136,6,22,10000,'2026-09-05','mobile_money');
INSERT INTO "cotisations" VALUES(137,6,23,10000,'2026-09-04','especes');
INSERT INTO "cotisations" VALUES(138,6,24,10000,'2026-09-05','mobile_money');
INSERT INTO "cotisations" VALUES(139,6,25,10000,'2026-09-05','mobile_money');
INSERT INTO "cotisations" VALUES(140,7,2,10000,'2026-09-11','especes');
INSERT INTO "cotisations" VALUES(141,7,3,10000,'2026-09-13','mobile_money');
INSERT INTO "cotisations" VALUES(142,7,4,10000,'2026-09-10','mobile_money');
INSERT INTO "cotisations" VALUES(143,7,5,10000,'2026-09-12','mobile_money');
INSERT INTO "cotisations" VALUES(144,7,6,10000,'2026-09-12','mobile_money');
INSERT INTO "cotisations" VALUES(145,7,7,10000,'2026-09-10','especes');
INSERT INTO "cotisations" VALUES(146,7,8,10000,'2026-09-17','mobile_money');
INSERT INTO "cotisations" VALUES(147,7,9,10000,'2026-09-10','mobile_money');
INSERT INTO "cotisations" VALUES(148,7,10,10000,'2026-09-10','mobile_money');
INSERT INTO "cotisations" VALUES(149,7,11,10000,'2026-09-11','especes');
INSERT INTO "cotisations" VALUES(150,7,12,10000,'2026-09-10','mobile_money');
INSERT INTO "cotisations" VALUES(151,7,14,10000,'2026-09-11','mobile_money');
INSERT INTO "cotisations" VALUES(152,7,15,10000,'2026-09-12','mobile_money');
INSERT INTO "cotisations" VALUES(153,7,16,10000,'2026-09-12','especes');
INSERT INTO "cotisations" VALUES(154,7,17,10000,'2026-09-12','especes');
INSERT INTO "cotisations" VALUES(155,7,18,10000,'2026-09-11','mobile_money');
INSERT INTO "cotisations" VALUES(156,7,20,10000,'2026-09-11','mobile_money');
INSERT INTO "cotisations" VALUES(157,7,21,10000,'2026-09-12','mobile_money');
INSERT INTO "cotisations" VALUES(158,7,22,10000,'2026-09-13','mobile_money');
INSERT INTO "cotisations" VALUES(159,7,23,10000,'2026-09-12','especes');
INSERT INTO "cotisations" VALUES(160,7,24,10000,'2026-09-15','especes');
INSERT INTO "cotisations" VALUES(161,7,25,10000,'2026-09-10','especes');
INSERT INTO "cotisations" VALUES(162,8,1,10000,'2026-09-17','mobile_money');
INSERT INTO "cotisations" VALUES(163,8,2,10000,'2026-09-19','mobile_money');
INSERT INTO "cotisations" VALUES(164,8,3,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(165,8,4,10000,'2026-09-19','mobile_money');
INSERT INTO "cotisations" VALUES(166,8,5,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(167,8,6,10000,'2026-09-25','especes');
INSERT INTO "cotisations" VALUES(168,8,8,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(169,8,9,10000,'2026-09-18','especes');
INSERT INTO "cotisations" VALUES(170,8,10,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(171,8,11,10000,'2026-09-17','mobile_money');
INSERT INTO "cotisations" VALUES(172,8,12,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(173,8,13,10000,'2026-09-18','especes');
INSERT INTO "cotisations" VALUES(174,8,14,10000,'2026-09-19','mobile_money');
INSERT INTO "cotisations" VALUES(175,8,15,10000,'2026-09-24','especes');
INSERT INTO "cotisations" VALUES(176,8,17,10000,'2026-09-19','mobile_money');
INSERT INTO "cotisations" VALUES(177,8,18,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(178,8,20,10000,'2026-09-23','mobile_money');
INSERT INTO "cotisations" VALUES(179,8,21,10000,'2026-09-18','especes');
INSERT INTO "cotisations" VALUES(180,8,22,10000,'2026-09-18','especes');
INSERT INTO "cotisations" VALUES(181,8,23,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(182,8,24,10000,'2026-09-17','mobile_money');
INSERT INTO "cotisations" VALUES(183,8,25,10000,'2026-09-18','mobile_money');
INSERT INTO "cotisations" VALUES(184,9,1,10000,'2026-09-25','especes');
INSERT INTO "cotisations" VALUES(185,9,2,10000,'2026-09-25','especes');
INSERT INTO "cotisations" VALUES(186,9,3,10000,'2026-09-24','mobile_money');
INSERT INTO "cotisations" VALUES(187,9,4,10000,'2026-10-01','mobile_money');
INSERT INTO "cotisations" VALUES(188,9,5,10000,'2026-09-25','mobile_money');
INSERT INTO "cotisations" VALUES(189,9,6,10000,'2026-09-27','mobile_money');
INSERT INTO "cotisations" VALUES(190,9,7,10000,'2026-09-24','mobile_money');
INSERT INTO "cotisations" VALUES(191,9,8,10000,'2026-09-25','mobile_money');
INSERT INTO "cotisations" VALUES(192,9,9,10000,'2026-09-25','mobile_money');
INSERT INTO "cotisations" VALUES(193,9,10,10000,'2026-09-26','mobile_money');
INSERT INTO "cotisations" VALUES(194,9,11,10000,'2026-09-25','mobile_money');
INSERT INTO "cotisations" VALUES(195,9,12,10000,'2026-09-26','mobile_money');
INSERT INTO "cotisations" VALUES(196,9,13,10000,'2026-10-01','especes');
INSERT INTO "cotisations" VALUES(197,9,14,10000,'2026-09-24','especes');
INSERT INTO "cotisations" VALUES(198,9,15,10000,'2026-09-28','especes');
INSERT INTO "cotisations" VALUES(199,9,16,10000,'2026-09-25','especes');
INSERT INTO "cotisations" VALUES(200,9,17,10000,'2026-09-30','mobile_money');
INSERT INTO "cotisations" VALUES(201,9,18,10000,'2026-09-26','mobile_money');
INSERT INTO "cotisations" VALUES(202,9,20,10000,'2026-09-25','mobile_money');
INSERT INTO "cotisations" VALUES(203,9,21,10000,'2026-09-24','mobile_money');
INSERT INTO "cotisations" VALUES(204,9,22,10000,'2026-09-26','mobile_money');
INSERT INTO "cotisations" VALUES(205,9,23,10000,'2026-09-29','especes');
INSERT INTO "cotisations" VALUES(206,9,24,10000,'2026-10-02','especes');
INSERT INTO "cotisations" VALUES(207,9,25,10000,'2026-09-24','mobile_money');
INSERT INTO "cotisations" VALUES(208,10,1,10000,'2026-10-01','mobile_money');
INSERT INTO "cotisations" VALUES(209,10,2,10000,'2026-10-02','mobile_money');
INSERT INTO "cotisations" VALUES(210,10,3,10000,'2026-10-03','mobile_money');
INSERT INTO "cotisations" VALUES(211,10,4,10000,'2026-10-03','mobile_money');
INSERT INTO "cotisations" VALUES(212,10,5,10000,'2026-10-02','mobile_money');
INSERT INTO "cotisations" VALUES(213,10,6,10000,'2026-10-02','especes');
INSERT INTO "cotisations" VALUES(214,10,7,10000,'2026-10-03','mobile_money');
INSERT INTO "cotisations" VALUES(215,10,8,10000,'2026-10-01','mobile_money');
INSERT INTO "cotisations" VALUES(216,10,9,10000,'2026-10-03','mobile_money');
INSERT INTO "cotisations" VALUES(217,10,10,10000,'2026-10-01','mobile_money');
INSERT INTO "cotisations" VALUES(218,10,11,10000,'2026-10-02','especes');
INSERT INTO "cotisations" VALUES(219,10,12,10000,'2026-10-02','especes');
INSERT INTO "cotisations" VALUES(220,10,13,10000,'2026-10-09','mobile_money');
INSERT INTO "cotisations" VALUES(221,10,15,10000,'2026-10-02','especes');
INSERT INTO "cotisations" VALUES(222,10,16,10000,'2026-10-03','especes');
INSERT INTO "cotisations" VALUES(223,10,17,10000,'2026-10-01','especes');
INSERT INTO "cotisations" VALUES(224,10,19,10000,'2026-10-06','mobile_money');
INSERT INTO "cotisations" VALUES(225,10,20,10000,'2026-10-01','mobile_money');
INSERT INTO "cotisations" VALUES(226,10,21,10000,'2026-10-01','especes');
INSERT INTO "cotisations" VALUES(227,10,22,10000,'2026-10-01','especes');
INSERT INTO "cotisations" VALUES(228,10,23,10000,'2026-10-03','especes');
INSERT INTO "cotisations" VALUES(229,10,24,10000,'2026-10-02','mobile_money');
INSERT INTO "cotisations" VALUES(230,10,25,10000,'2026-10-03','especes');
INSERT INTO "cotisations" VALUES(231,11,2,10000,'2026-10-10','mobile_money');
INSERT INTO "cotisations" VALUES(232,11,4,10000,'2026-10-09','mobile_money');
INSERT INTO "cotisations" VALUES(233,11,5,10000,'2026-10-10','especes');
INSERT INTO "cotisations" VALUES(234,11,6,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(235,11,7,10000,'2026-10-09','especes');
INSERT INTO "cotisations" VALUES(236,11,8,10000,'2026-10-09','especes');
INSERT INTO "cotisations" VALUES(237,11,10,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(238,11,11,10000,'2026-10-09','especes');
INSERT INTO "cotisations" VALUES(239,11,12,10000,'2026-10-10','mobile_money');
INSERT INTO "cotisations" VALUES(240,11,13,10000,'2026-10-09','mobile_money');
INSERT INTO "cotisations" VALUES(241,11,14,10000,'2026-10-12','mobile_money');
INSERT INTO "cotisations" VALUES(242,11,15,10000,'2026-10-14','especes');
INSERT INTO "cotisations" VALUES(243,11,16,10000,'2026-10-10','mobile_money');
INSERT INTO "cotisations" VALUES(244,11,17,10000,'2026-10-13','mobile_money');
INSERT INTO "cotisations" VALUES(245,11,18,10000,'2026-10-10','mobile_money');
INSERT INTO "cotisations" VALUES(246,11,19,10000,'2026-10-08','especes');
INSERT INTO "cotisations" VALUES(247,11,20,10000,'2026-10-10','mobile_money');
INSERT INTO "cotisations" VALUES(248,11,22,10000,'2026-10-08','especes');
INSERT INTO "cotisations" VALUES(249,11,25,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(250,12,1,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(251,12,2,10000,'2026-10-19','especes');
INSERT INTO "cotisations" VALUES(252,12,3,10000,'2026-10-17','mobile_money');
INSERT INTO "cotisations" VALUES(253,12,4,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(254,12,5,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(255,12,6,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(256,12,8,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(257,12,10,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(258,12,11,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(259,12,12,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(260,12,13,10000,'2026-10-17','mobile_money');
INSERT INTO "cotisations" VALUES(261,12,14,10000,'2026-10-15','especes');
INSERT INTO "cotisations" VALUES(262,12,15,10000,'2026-10-15','especes');
INSERT INTO "cotisations" VALUES(263,12,16,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(264,12,17,10000,'2026-10-15','especes');
INSERT INTO "cotisations" VALUES(265,12,19,10000,'2026-10-17','mobile_money');
INSERT INTO "cotisations" VALUES(266,12,20,10000,'2026-10-16','especes');
INSERT INTO "cotisations" VALUES(267,12,21,10000,'2026-10-15','mobile_money');
INSERT INTO "cotisations" VALUES(268,12,22,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(269,12,23,10000,'2026-10-16','mobile_money');
INSERT INTO "cotisations" VALUES(270,12,24,10000,'2026-10-17','especes');
INSERT INTO "cotisations" VALUES(271,12,25,10000,'2026-10-22','mobile_money');
INSERT INTO "cotisations" VALUES(272,13,14,10000,'2026-10-21','mobile_money');
INSERT INTO "cotisations" VALUES(273,13,12,10000,'2026-10-21','mobile_money');
INSERT INTO "cotisations" VALUES(274,13,22,10000,'2026-10-21','especes');
INSERT INTO "cotisations" VALUES(275,13,25,10000,'2026-10-21','mobile_money');
INSERT INTO "cotisations" VALUES(276,13,2,10000,'2026-10-21','mobile_money');
INSERT INTO "cotisations" VALUES(277,13,10,10000,'2026-10-21','especes');
INSERT INTO "cotisations" VALUES(278,13,20,10000,'2026-10-21','especes');
INSERT INTO "cotisations" VALUES(279,13,24,10000,'2026-10-21','mobile_money');
INSERT INTO "cotisations" VALUES(280,13,4,10000,'2026-10-21','especes');
CREATE TABLE cycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    montant_cotisation INTEGER NOT NULL CHECK (montant_cotisation > 0),
    periodicite TEXT NOT NULL CHECK (periodicite IN ('hebdomadaire', 'mensuelle')),
    date_debut TEXT NOT NULL
);
INSERT INTO "cycles" VALUES(1,'Cycle 2026-2027',10000,'hebdomadaire','2026-08-01');
CREATE TABLE demandes_adhesion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL CHECK (length(nom) >= 3),
    telephone TEXT NOT NULL
        CHECK (telephone GLOB '6[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    message TEXT,
    date_demande TEXT NOT NULL,
    statut TEXT NOT NULL DEFAULT 'en_attente'
        CHECK (statut IN ('en_attente', 'acceptee', 'refusee'))
);
CREATE TABLE membres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL CHECK (length(nom) >= 3),
    telephone TEXT NOT NULL UNIQUE
        CHECK (telephone GLOB '6[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    date_adhesion TEXT NOT NULL,
    empreinte TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'membre'
        CHECK (role IN ('membre', 'tresorier', 'president')),
    actif INTEGER NOT NULL DEFAULT 1 CHECK (actif IN (0, 1))
);
INSERT INTO "membres" VALUES(1,'Mbarga Jean-Pierre','677000001','2024-10-06','scrypt:32768:8:1$OUVgCmWuGMpzl4AE$a3921337fb973ea0edaa64d38a3b845bd10afdf9149cf35e1706b7b34474e1c2a3e2f2eedccef309888acbc0d97985e656c80cb0b20cde1c540aa0372365254a','tresorier',1);
INSERT INTO "membres" VALUES(2,'Ngo Bassa Colette','677000002','2026-03-30','scrypt:32768:8:1$9e8GnTz5rQTYX1Tq$1f790dbf11541a0f69a43c3787fe9d9625b66109785e561265bff40acea97ca8532dd0495e8c7b1abbe45352de40f7316d31b798880942309cf2b7aeb70617bf','president',1);
INSERT INTO "membres" VALUES(3,'Fotso Alphonse','677000003','2026-06-27','scrypt:32768:8:1$MJGU9icx6pgSJ9Cj$acf28672e036187bfcff0bfde05af61823ded0902eaa971cd15f1d9fe831eee6b2efd45bfd8300c99c10836fe834bf547ffdbff9531b791b7eaf43ff437c7025','membre',1);
INSERT INTO "membres" VALUES(4,'Atangana Rose','677000004','2025-10-14','scrypt:32768:8:1$MZ0RPOF4y106sITO$ac5b7d9318747d8c5e23280ead9e3ac7b27c1940143ac6cbd6df29837f099528d5d89da0ccc58d08edd2b159b9a5317da29c0f8445c1ef6116a7ee3bf24a6c26','membre',1);
INSERT INTO "membres" VALUES(5,'Njoya Ibrahim','677000005','2025-11-14','scrypt:32768:8:1$66QqsHMBoh8Ow6fu$463ba1da80e6917ebb1edbbd272c4f59a67f1968f1a9b18a073afc4c0b56766c18c40917ba3a59132ae41e107530485b286d0c9738a0c3b6400efd34690ec2e2','membre',1);
INSERT INTO "membres" VALUES(6,'Ekane Sandra','677000006','2025-12-06','scrypt:32768:8:1$pT4fij17f6sEjtHy$a5d4a33c7283247e5839ec2737af342074f0eb11574a598803c21701607a9719743773f975c4f91ac74791788df3983728b67898dbdb8a19b3b15694c5901aca','membre',1);
INSERT INTO "membres" VALUES(7,'Tchoupo Marcel','677000007','2026-03-02','scrypt:32768:8:1$Ceg77cb4kETFsP5R$d6ec3a3d0db335a0e75b142b6ebf33b9f248a1f1f62492c2c836998507fab469dc25bc92ae532ef9911a17093d7dff0d8b9441d6ba4e57c1f288af1de3ec2b9a','membre',1);
INSERT INTO "membres" VALUES(8,'Bello Moussa','677000008','2026-04-09','scrypt:32768:8:1$ZQO9ZpBU3rrRR8gQ$7c37ec9c5db85600ac4feadf97cc55518f6eca69535016ee24d9551fcbe4bae787558107a296f9e60250e33fcfe5769c48fa92d51a7491e39c720a85508b5651','membre',1);
INSERT INTO "membres" VALUES(9,'Kamga Hélène','677000009','2025-01-10','scrypt:32768:8:1$HVoikZhOGgWLKjCH$d48ee7e8763c6e436f48ad5dbc27fdfadd154bc2483a9bc7d5e37098997e1039f88c8baa68b216735d63f1f019db9853bda5c5f174e9bcb86db9656199b0e8cc','membre',1);
INSERT INTO "membres" VALUES(10,'Nkoulou Pascal','677000010','2026-04-24','scrypt:32768:8:1$ZRJYHVafvAaovTrB$571e1f87c7a156353b2e774cf63bc30ab9555a012cce858484e7008bf207d82628e3327abe33b99b6e92a34dfd3795a8739989c6ce8f055c8ddcf75de93bfa6f','membre',1);
INSERT INTO "membres" VALUES(11,'Mvondo Estelle','677000011','2024-11-25','scrypt:32768:8:1$fcrAz8yGzB09MecM$617878780b935c0aac7d6811e65090bad71abb16057b59cbc9bb5f15fd199b4c6ffa23be1e7457de61ea546572e2f8c112b595fb51b4100398be2f2eb239b7e2','membre',1);
INSERT INTO "membres" VALUES(12,'Tagne Brice','677000012','2025-05-16','scrypt:32768:8:1$KLj20DdxbXHlby1W$e22c374894d178dcc639f17258c52ae223acf9e80943edd5065e9680caacb5aeaeddd138ac7a3282bcad7fd97e739097df5a1d9a38b1be447e61b048cc661304','membre',1);
INSERT INTO "membres" VALUES(13,'Ndongo Mireille','677000013','2026-06-20','scrypt:32768:8:1$M4El5lBDa8KO4Zu6$274f88c0afc7e89fba09ba5fe357137702ce2bb5261ee37bfb613ec9927fa6df3b8a512074a53f15ccbe4a022edc5bea6dcaf77e9094b485568279e0e40b8cc9','membre',1);
INSERT INTO "membres" VALUES(14,'Essomba Charles','677000014','2026-06-22','scrypt:32768:8:1$gQMR575huuP3fDq3$905b20b3c20eb97dcd9a9d6e29f66068ee2c922db92e05412db757adfec0fde64b77cc37b48b7f6ad41c80d8b35893bf54992b5737be177090d6dfae42a82ffd','membre',1);
INSERT INTO "membres" VALUES(15,'Fouda Yvette','677000015','2026-04-18','scrypt:32768:8:1$GhcGGMNX3f6gdZ4e$02de784f5bd057398832d5c41f965526a2d3bcd5f821b905db09be739dafaf967984493f6d3c66443fa266bf858e549ca4659befd707a436cd5402a51c2b82a9','membre',1);
INSERT INTO "membres" VALUES(16,'Kenmogne Aurélien','677000016','2025-12-11','scrypt:32768:8:1$Fd2Y6yTn4VnI0zvR$fb1237e9f8bc2137f7bc53f74010223f7cef507815f164f800548d19ddcfb8ebbe308544619e05dd2b09a5f913a84741bfe7a4aa61c71670b401ab45827cafe5','membre',1);
INSERT INTO "membres" VALUES(17,'Abena Solange','677000017','2025-11-26','scrypt:32768:8:1$v1jTZ7SrCeKO1oIv$9c0231eb7a0b0cf96548daafb9b0324072d971b83e2781ee821973660c0e94df6d238767e2891b1009d4bfd559bcc8ac9f792c309d4c20ccde95e7b157bc5986','membre',1);
INSERT INTO "membres" VALUES(18,'Mballa Désiré','677000018','2025-02-20','scrypt:32768:8:1$aidSg2ISJ8ryZnhU$43b5a6ff086f40028574b29880ee354f9de7a93e4ac37ad296a5711fe5011b96fbf71741c9e0786a97aaccb86167feb82310ac9ef5b1c78424bb1cdc3ef9d908','membre',1);
INSERT INTO "membres" VALUES(19,'Ngassa Pauline','677000019','2024-11-13','scrypt:32768:8:1$gJdE54olp6DQ91do$8b8e086246408f02f2653d89cf2244701b4042aa748ebcb14d3ff51a6269afb5128237fb899a9a0336ac7f7cafed77abfd344159ae156d23342ee7ee4fe29327','membre',1);
INSERT INTO "membres" VALUES(20,'Wouapi Thierry','677000020','2026-06-25','scrypt:32768:8:1$m5Ykn0YlEX8V0iKa$beb51d24478f08e7b2a0fd3a258f00c41f146b69b69b1426c4e5e8d300b1d25c71cd675f4905cffd41fc50abcf3d4b74263e32c403d155dae9cbc4eca282dc6e','membre',1);
INSERT INTO "membres" VALUES(21,'Biyong Carine','677000021','2024-12-25','scrypt:32768:8:1$OR9Ri4POTsWsZECK$f00f5b8de1d9c14dc3cb5c7fd2e527117927733c5ab6787a0f3c687bcf85f1bee49c1de2f210d24aa4d225fe3293718636f9b8b47c0e04da9583de8d3d35a047','membre',1);
INSERT INTO "membres" VALUES(22,'Tchinda Roland','677000022','2025-12-31','scrypt:32768:8:1$mzkWHwRYlCGFijKv$b9e1083e2bf248c5307200143793f1cf1b7c71e3ec6cb600043e05b812d7f2ed400a70e594cef6e95e19c82f01258670e57d0938185fa01ba18cd61c92723235','membre',1);
INSERT INTO "membres" VALUES(23,'Onana Félicité','677000023','2024-09-25','scrypt:32768:8:1$mcEWOh9xKuKAXSar$8a0ac78e51ea92b517b20bfbb538483bd9df586ed5ef1e7e9077d67122abbb42a4e7ac5cc1cb8a76e2d11e648754cfc2ff3b3807007c92c7435daba311521ba8','membre',1);
INSERT INTO "membres" VALUES(24,'Djoumessi Patrick','677000024','2025-01-10','scrypt:32768:8:1$ffmP2r6moiFzm1mB$88195d0a9e3ff75cc8777e4b7ef41beddbb34f32a3fdee25b77b3f3caf4e5fc4bf45bf669956054b8666ef485e0b1943d20d8d4f3e7557e9bc3ac2fe6c4f09b5','membre',1);
INSERT INTO "membres" VALUES(25,'Nana Laurette','677000025','2025-05-19','scrypt:32768:8:1$ohgHMT9myYT220Od$7996de0dba3a0dd3583fe9c618054aa2af99ad6eb46c76e654bd3ade220a83dd1454879d890f826dac59042fdb83a3168f4eb560600ab6b517660dd494ce6a1c','membre',1);
CREATE TABLE penalites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    membre_id INTEGER NOT NULL REFERENCES membres(id),
    seance_id INTEGER NOT NULL REFERENCES seances(id) ON DELETE CASCADE,
    motif TEXT NOT NULL CHECK (motif IN ('retard', 'absence')),
    montant INTEGER NOT NULL CHECK (montant > 0),
    payee INTEGER NOT NULL DEFAULT 0 CHECK (payee IN (0, 1)),
    UNIQUE (membre_id, seance_id, motif)
);
INSERT INTO "penalites" VALUES(1,23,1,'retard',500,0);
INSERT INTO "penalites" VALUES(2,24,1,'absence',1000,0);
INSERT INTO "penalites" VALUES(3,1,2,'retard',500,1);
INSERT INTO "penalites" VALUES(4,2,2,'retard',500,1);
INSERT INTO "penalites" VALUES(5,18,2,'retard',500,1);
INSERT INTO "penalites" VALUES(6,19,2,'retard',500,1);
INSERT INTO "penalites" VALUES(7,25,2,'retard',500,1);
INSERT INTO "penalites" VALUES(8,1,3,'absence',1000,1);
INSERT INTO "penalites" VALUES(9,8,3,'retard',500,1);
INSERT INTO "penalites" VALUES(10,11,3,'retard',500,0);
INSERT INTO "penalites" VALUES(11,20,3,'retard',500,1);
INSERT INTO "penalites" VALUES(12,22,3,'retard',500,1);
INSERT INTO "penalites" VALUES(13,4,4,'retard',500,0);
INSERT INTO "penalites" VALUES(14,11,4,'retard',500,1);
INSERT INTO "penalites" VALUES(15,20,4,'retard',500,0);
INSERT INTO "penalites" VALUES(16,25,4,'retard',500,0);
INSERT INTO "penalites" VALUES(17,4,5,'retard',500,0);
INSERT INTO "penalites" VALUES(18,4,6,'retard',500,0);
INSERT INTO "penalites" VALUES(19,5,6,'retard',500,0);
INSERT INTO "penalites" VALUES(20,13,6,'retard',500,1);
INSERT INTO "penalites" VALUES(21,19,6,'retard',500,0);
INSERT INTO "penalites" VALUES(22,20,6,'absence',1000,0);
INSERT INTO "penalites" VALUES(23,8,7,'retard',500,1);
INSERT INTO "penalites" VALUES(24,19,7,'absence',1000,0);
INSERT INTO "penalites" VALUES(25,22,7,'retard',500,0);
INSERT INTO "penalites" VALUES(26,20,8,'retard',500,1);
INSERT INTO "penalites" VALUES(27,13,9,'retard',500,1);
INSERT INTO "penalites" VALUES(28,15,9,'retard',500,1);
INSERT INTO "penalites" VALUES(29,19,9,'absence',1000,0);
INSERT INTO "penalites" VALUES(30,24,9,'retard',500,1);
INSERT INTO "penalites" VALUES(31,13,10,'retard',500,1);
INSERT INTO "penalites" VALUES(32,6,11,'retard',500,1);
INSERT INTO "penalites" VALUES(33,9,11,'absence',1000,1);
INSERT INTO "penalites" VALUES(34,14,11,'retard',500,0);
INSERT INTO "penalites" VALUES(35,23,11,'absence',1000,1);
INSERT INTO "penalites" VALUES(36,25,11,'retard',500,0);
INSERT INTO "penalites" VALUES(37,2,12,'retard',500,1);
CREATE TABLE seances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id INTEGER NOT NULL REFERENCES cycles(id) ON DELETE CASCADE,
    numero INTEGER NOT NULL CHECK (numero >= 1),
    date TEXT NOT NULL,
    beneficiaire_id INTEGER REFERENCES membres(id),
    montant_total INTEGER NOT NULL DEFAULT 0 CHECK (montant_total >= 0),
    UNIQUE (cycle_id, numero),
    UNIQUE (cycle_id, beneficiaire_id)
);
INSERT INTO "seances" VALUES(1,1,1,'2026-08-01',24,230000);
INSERT INTO "seances" VALUES(2,1,2,'2026-08-08',17,230000);
INSERT INTO "seances" VALUES(3,1,3,'2026-08-15',21,240000);
INSERT INTO "seances" VALUES(4,1,4,'2026-08-22',25,230000);
INSERT INTO "seances" VALUES(5,1,5,'2026-08-29',16,240000);
INSERT INTO "seances" VALUES(6,1,6,'2026-09-05',3,220000);
INSERT INTO "seances" VALUES(7,1,7,'2026-09-12',10,220000);
INSERT INTO "seances" VALUES(8,1,8,'2026-09-19',23,220000);
INSERT INTO "seances" VALUES(9,1,9,'2026-09-26',18,240000);
INSERT INTO "seances" VALUES(10,1,10,'2026-10-03',7,230000);
INSERT INTO "seances" VALUES(11,1,11,'2026-10-10',12,190000);
INSERT INTO "seances" VALUES(12,1,12,'2026-10-17',2,220000);
INSERT INTO "seances" VALUES(13,1,13,'2026-10-24',20,90000);
INSERT INTO "seances" VALUES(14,1,14,'2026-10-31',13,0);
INSERT INTO "seances" VALUES(15,1,15,'2026-11-07',4,0);
INSERT INTO "seances" VALUES(16,1,16,'2026-11-14',5,0);
INSERT INTO "seances" VALUES(17,1,17,'2026-11-21',22,0);
INSERT INTO "seances" VALUES(18,1,18,'2026-11-28',11,0);
INSERT INTO "seances" VALUES(19,1,19,'2026-12-05',14,0);
INSERT INTO "seances" VALUES(20,1,20,'2026-12-12',6,0);
INSERT INTO "seances" VALUES(21,1,21,'2026-12-19',1,0);
INSERT INTO "seances" VALUES(22,1,22,'2026-12-26',9,0);
INSERT INTO "seances" VALUES(23,1,23,'2027-01-02',NULL,0);
INSERT INTO "seances" VALUES(24,1,24,'2027-01-09',NULL,0);
INSERT INTO "seances" VALUES(25,1,25,'2027-01-16',NULL,0);
CREATE UNIQUE INDEX idx_demande_attente ON demandes_adhesion (telephone)
    WHERE statut = 'en_attente';
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('administrateurs',1);
INSERT INTO "sqlite_sequence" VALUES('membres',25);
INSERT INTO "sqlite_sequence" VALUES('cycles',1);
INSERT INTO "sqlite_sequence" VALUES('seances',25);
INSERT INTO "sqlite_sequence" VALUES('cotisations',280);
INSERT INTO "sqlite_sequence" VALUES('penalites',37);
COMMIT;