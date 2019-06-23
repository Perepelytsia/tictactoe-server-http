--
-- PostgreSQL database dump
--

-- Dumped from database version 10.8 (Ubuntu 10.8-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.8 (Ubuntu 10.8-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: commands; Type: TABLE; Schema: public; Owner: tictactoe
--

CREATE TABLE public.commands (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP(0),
    type character(3) NOT NULL,
    cmd character varying(6) NOT NULL,
    owner character varying(10) NOT NULL,
    data json NOT NULL
);


ALTER TABLE public.commands OWNER TO tictactoe;

--
-- Name: commands_id_seq; Type: SEQUENCE; Schema: public; Owner: tictactoe
--

CREATE SEQUENCE public.commands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.commands_id_seq OWNER TO tictactoe;

--
-- Name: commands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tictactoe
--

ALTER SEQUENCE public.commands_id_seq OWNED BY public.commands.id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: tictactoe
--

CREATE TABLE public.games (
    id integer NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP(0),
    active smallint NOT NULL,
    turn smallint NOT NULL,
    chip smallint NOT NULL,
    owner character varying(20) NOT NULL,
    opponet character varying(20) NOT NULL,
    field json NOT NULL,
    result smallint
);


ALTER TABLE public.games OWNER TO tictactoe;

--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: tictactoe
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.games_id_seq OWNER TO tictactoe;

--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tictactoe
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: tictactoe
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    win integer DEFAULT 0 NOT NULL,
    lost integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.users OWNER TO tictactoe;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: tictactoe
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO tictactoe;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tictactoe
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: commands id; Type: DEFAULT; Schema: public; Owner: tictactoe
--

ALTER TABLE ONLY public.commands ALTER COLUMN id SET DEFAULT nextval('public.commands_id_seq'::regclass);


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: tictactoe
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: tictactoe
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: commands commands_pkey; Type: CONSTRAINT; Schema: public; Owner: tictactoe
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_pkey PRIMARY KEY (id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: tictactoe
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tictactoe
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

