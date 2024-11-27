--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: households; Type: TABLE; Schema: public; Owner: sam
--

CREATE TABLE public.households (
    household_id integer NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.households OWNER TO sam;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: sam
--

CREATE TABLE public.order_items (
    item_id integer NOT NULL,
    student_id integer NOT NULL,
    price money NOT NULL,
    quantity integer,
    added_at timestamp without time zone NOT NULL,
    product_id integer NOT NULL
);


ALTER TABLE public.order_items OWNER TO sam;

--
-- Name: products; Type: TABLE; Schema: public; Owner: sam
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name character varying(255) NOT NULL,
    price money NOT NULL,
    availability boolean,
    supermarket_id integer NOT NULL
);


ALTER TABLE public.products OWNER TO sam;

--
-- Name: student; Type: TABLE; Schema: public; Owner: sam
--

CREATE TABLE public.student (
    student_id integer NOT NULL,
    student_name character varying(50) NOT NULL,
    household_id integer NOT NULL,
    email character varying(255) NOT NULL
);


ALTER TABLE public.student OWNER TO sam;

--
-- Data for Name: households; Type: TABLE DATA; Schema: public; Owner: sam
--

COPY public.households (household_id, address) FROM stdin;
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: sam
--

COPY public.order_items (item_id, student_id, price, quantity, added_at, product_id) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: sam
--

COPY public.products (product_id, product_name, price, availability, supermarket_id) FROM stdin;
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: sam
--

COPY public.student (student_id, student_name, household_id, email) FROM stdin;
\.


--
-- Name: households households_pkey; Type: CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.households
    ADD CONSTRAINT households_pkey PRIMARY KEY (household_id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (item_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: student student_email_key; Type: CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_email_key UNIQUE (email);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (student_id);


--
-- Name: student fk_household; Type: FK CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT fk_household FOREIGN KEY (household_id) REFERENCES public.households(household_id);


--
-- Name: order_items fk_product_id; Type: FK CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: order_items fk_student_id; Type: FK CONSTRAINT; Schema: public; Owner: sam
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_student_id FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- PostgreSQL database dump complete
--

