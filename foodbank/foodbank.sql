--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: food_lock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE food_lock (
    lock_id integer NOT NULL,
    fid integer,
    food_quantity integer,
    status text DEFAULT 'not_picked'::text,
    ngo_id integer,
    timelimit integer
);


--
-- Name: food_lock_lock_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE food_lock_lock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: food_lock_lock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE food_lock_lock_id_seq OWNED BY food_lock.lock_id;


--
-- Name: food_unlock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE food_unlock (
    unlock_id integer NOT NULL,
    fid integer,
    quantity integer
);


--
-- Name: food_unlock_unlock_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE food_unlock_unlock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: food_unlock_unlock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE food_unlock_unlock_id_seq OWNED BY food_unlock.unlock_id;


--
-- Name: foodinfo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE foodinfo (
    id integer,
    foodid integer NOT NULL,
    foodquantity integer,
    description text,
    duration integer,
    created_timestamp timestamp with time zone DEFAULT now()
);


--
-- Name: foodinfo_foodid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE foodinfo_foodid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foodinfo_foodid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE foodinfo_foodid_seq OWNED BY foodinfo.foodid;


--
-- Name: userinfo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE userinfo (
    userid integer NOT NULL,
    type text,
    location text,
    email text,
    password text,
    name text,
    phone bigint
);


--
-- Name: userinfo_userid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE userinfo_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: userinfo_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE userinfo_userid_seq OWNED BY userinfo.userid;


--
-- Name: food_lock lock_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_lock ALTER COLUMN lock_id SET DEFAULT nextval('food_lock_lock_id_seq'::regclass);


--
-- Name: food_unlock unlock_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_unlock ALTER COLUMN unlock_id SET DEFAULT nextval('food_unlock_unlock_id_seq'::regclass);


--
-- Name: foodinfo foodid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY foodinfo ALTER COLUMN foodid SET DEFAULT nextval('foodinfo_foodid_seq'::regclass);


--
-- Name: userinfo userid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY userinfo ALTER COLUMN userid SET DEFAULT nextval('userinfo_userid_seq'::regclass);


--
-- Data for Name: food_lock; Type: TABLE DATA; Schema: public; Owner: -
--

COPY food_lock (lock_id, fid, food_quantity, status, ngo_id, timelimit) FROM stdin;
28	85	50	obsolete	41	4
\.


--
-- Data for Name: food_unlock; Type: TABLE DATA; Schema: public; Owner: -
--

COPY food_unlock (unlock_id, fid, quantity) FROM stdin;
76	85	100
\.


--
-- Data for Name: foodinfo; Type: TABLE DATA; Schema: public; Owner: -
--

COPY foodinfo (id, foodid, foodquantity, description, duration, created_timestamp) FROM stdin;
40	85	100	Paneer,rice,fruits	9	2018-02-27 04:26:21.324586-05
\.


--
-- Data for Name: userinfo; Type: TABLE DATA; Schema: public; Owner: -
--

COPY userinfo (userid, type, location, email, password, name, phone) FROM stdin;
40	hotel	Kukatpally,Hyderabad	\N	123456789	chutneys	8179721639
41	ngo	Kukatpally,Hyderabad	\N	123456789	AkashyaPatra	8019945706
\.


--
-- Name: food_lock_lock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('food_lock_lock_id_seq', 28, true);


--
-- Name: food_unlock_unlock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('food_unlock_unlock_id_seq', 76, true);


--
-- Name: foodinfo_foodid_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('foodinfo_foodid_seq', 85, true);


--
-- Name: userinfo_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('userinfo_userid_seq', 41, true);


--
-- Name: food_lock food_lock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_lock
    ADD CONSTRAINT food_lock_pkey PRIMARY KEY (lock_id);


--
-- Name: food_unlock food_unlock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_unlock
    ADD CONSTRAINT food_unlock_pkey PRIMARY KEY (unlock_id);


--
-- Name: foodinfo foodinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY foodinfo
    ADD CONSTRAINT foodinfo_pkey PRIMARY KEY (foodid);


--
-- Name: userinfo userinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY userinfo
    ADD CONSTRAINT userinfo_pkey PRIMARY KEY (userid);


--
-- Name: food_lock food_lock_fid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_lock
    ADD CONSTRAINT food_lock_fid_fkey FOREIGN KEY (fid) REFERENCES foodinfo(foodid);


--
-- Name: food_lock food_lock_ngo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_lock
    ADD CONSTRAINT food_lock_ngo_id_fkey FOREIGN KEY (ngo_id) REFERENCES userinfo(userid);


--
-- Name: food_unlock food_unlock_fid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY food_unlock
    ADD CONSTRAINT food_unlock_fid_fkey FOREIGN KEY (fid) REFERENCES foodinfo(foodid);


--
-- Name: foodinfo foodinfo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY foodinfo
    ADD CONSTRAINT foodinfo_id_fkey FOREIGN KEY (id) REFERENCES userinfo(userid);


--
-- PostgreSQL database dump complete
--

