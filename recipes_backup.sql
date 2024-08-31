--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    image_url character varying(200) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredients (
    id integer NOT NULL,
    description character varying(50) NOT NULL,
    recipe_id integer NOT NULL
);


ALTER TABLE public.ingredients OWNER TO postgres;

--
-- Name: ingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingredients_id_seq OWNER TO postgres;

--
-- Name: ingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingredients_id_seq OWNED BY public.ingredients.id;


--
-- Name: recipes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recipes (
    id integer NOT NULL,
    title character varying NOT NULL,
    description character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    image_url character varying NOT NULL,
    servings integer,
    prep_time integer,
    prep_time_unit character varying(10),
    cook_time integer,
    cook_time_unit character varying(10),
    user_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.recipes OWNER TO postgres;

--
-- Name: recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recipes_id_seq OWNER TO postgres;

--
-- Name: recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;


--
-- Name: steps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.steps (
    id integer NOT NULL,
    description text NOT NULL,
    order_num integer NOT NULL,
    recipe_id integer NOT NULL
);


ALTER TABLE public.steps OWNER TO postgres;

--
-- Name: steps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.steps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.steps_id_seq OWNER TO postgres;

--
-- Name: steps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.steps_id_seq OWNED BY public.steps.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(120) NOT NULL,
    password character varying NOT NULL,
    profile_image bytea NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: ingredients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);


--
-- Name: recipes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);


--
-- Name: steps id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.steps ALTER COLUMN id SET DEFAULT nextval('public.steps_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, image_url) FROM stdin;
1	Bebidas	/static/images/drink.webp
2	Entradas	/static/images/starter-dish.webp
3	Platos principales	/static/images/main-dish.webp
4	Postres	/static/images/dessert.webp
5	Otros	/static/images/others.webp
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingredients (id, description, recipe_id) FROM stdin;
1	1 huevo	1
2	15 cdas de azúcar	1
3	15 cdas de leche	1
4	15 cdas de aceite	1
5	15 cdas de harina leudante	1
6	250 gr de harina común 0000	2
7	7 gr. de levadura tipo Royal	2
8	80 ml de leche	2
9	1 yema de huevo	2
10	60 gr de manteca	2
11	35 - 45 gr de azúcar	2
12	escencia de vainilla	2
13	1 pizca de sal	2
14	200 gr. de azúcar	3
15	200 cc. de aceite neutro	3
16	2 huevos	3
17	350 gr. de harina leudante	3
18	Ralladura y jugo de 1 limón	3
19	1 kg. de carne picada	4
20	2 cebollas	4
21	2 tomates	4
22	5 limones	4
23	4 paquetes de tapas de empanadas	4
24	sal y pimienta	4
25	1 cda. de manteca	5
26	1 cda. de maizena	5
27	1 taza de leche	5
28	2 huevos	6
29	250 ml. de leche	6
30	100 gr. de harina	6
31	1 pizca de sal	6
32	1/2 cda. de manteca	6
33	Una colita de cuadril grande.	7
34	100 gr. de manteca.	7
35	200 gr. de mostaza de hierbas.	7
36	200 gr. de harina.	7
37	3 dientes de ajo picados.	7
38	2 papas blanqueadas con cáscara.	7
39	Romero fresco.	7
40	Aceite de oliva.	7
41	Sal y pimienta, a gusto.	7
42	400 gr. harina de fuerza	8
43	300 - 320 gr. de agua	8
44	6 gr. levadura fresca	8
45	7 gr. sal	8
46	250 gr. de carne picada	9
47	1 cebolla mediana	9
48	1 zanahoria pequeña	9
49	1/4 de pimiento morón	9
50	180-200 gr. de nidos de pasta o espaguetis	9
51	600 ml. de zumo de tomate	9
52	2 cdas. de aceite	9
53	sal, pimienta negra molida, especias al gusto	9
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recipes (id, title, description, created_at, image_url, servings, prep_time, prep_time_unit, cook_time, cook_time_unit, user_id, category_id) FROM stdin;
1	Torta 15 cucharadas	Esta receta de torta 15 cucharadas se adapta a cualquier situación, ya sea para una merienda o como torta de cumpleaños. Este bizcochuelo se hace con solo 5 ingredientes y una cuchara, sin dificultad alguna.	2024-08-12 13:16:55.544	/static/uploads/20240812101655_9a0fe0fa.webp	\N	\N	minutos	\N	minutos	1	4
2	Galletas de leche	Unas galletas ideales para acompañar un té, café o un vaso de leche con cacao, por ejemplo.	2024-08-13 13:46:36.976	/static/uploads/20240813104912_23159939.webp	5	20	minutos	25	minutos	1	5
3	Budín de limón esponjoso SIN manteca	Budín idéntico al de Starbucks, super esponjoso alto y lleno de sabor a limón es super rápido de hacer.	2024-08-21 13:48:04.199	/static/uploads/20240821104802_6ecc29e7.webp	16	15	minutos	35	minutos	1	4
4	Empanadas árables (económicas)	Las empanadas árabes o Fatay, como se las suele llamar popularmente, son un estandarte flamante de la cocina egipcia, palestina y sirio-libanesa. 	2024-08-21 13:54:27.218	/static/uploads/20240821105426_65743b7f.webp	56	2	horas	15	minutos	1	3
5	Salsa blanca	La salsa bechamel o salsa blanca es perfecta para pastas. Se usa para recetas como lasaña, canelones, pastas gratinadas o para mezclar con verduras como las espinacas.	2024-08-21 13:58:10.795	/static/uploads/20240821105810_5cbd978d.webp	\N	10	minutos	5	minutos	1	3
6	Panqueques	Fáciles y prácticos para comidas dulces o saladas!! Riquísimos!!	2024-08-21 14:04:12.824	/static/uploads/20240821110412_953d907f.webp	\N	\N	minutos	\N	minutos	1	4
7	Colita de cuadril a la mostaza	Una carne ideal para cocinar en cualquier momento del año, con un toque de sabor muy especial.	2024-08-21 14:16:25.276	/static/uploads/20240821111625_5e19a9f1.webp	\N	\N	minutos	30	minutos	1	3
8	Pan de barra stirato	Receta muy fácil de pan sin amasar.	2024-08-21 14:28:48.803	/static/uploads/20240821112848_c65f767f.webp	8	13	horas	20	minutos	1	5
9	Pasta con salsa de carne	Hoy preparamos un plato de pasta con salsa de carne riquísimo que se hace en 20 minutos y de forma muy sencilla.	2024-08-21 14:36:17.033	/static/uploads/20240821113616_addd572c.webp	2	5	minutos	15	minutos	1	3
\.


--
-- Data for Name: steps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.steps (id, description, order_num, recipe_id) FROM stdin;
1	Como primer paso, en un bowl vas a poner el huevo, junto con las 15 cucharadas de leche y las 15 de azúcar. Luego batir enérgicamente para que todo se integre y se forme una especie de crema. 	1	1
2	A continuación, deberás añadir el aceite y volver a mezclar para que se mezclen bien todos los líquidos. En este momento podés saborizar la preparación, por lo que podés incorporar esencia de vainilla, chocolate, alguna fruta como manzana o ralladura de algún cítrico como naranja o limón.	2	1
3	Cuando tengas los líquidos y el sabor bien mezclados, sumar las 15 cucharadas de harina leudante y mezclar bien hasta integrar y que no queden grumos.	3	1
4	Colocar en un molde enmantecado y enharinado la mezcla y, si se desea, sumar la cubierta azucarada (esto le dará una costra crocante al bizcocho).	4	1
5	Cocinar a horno bajo durante 45 minutos o hasta que pinchando la torta con un palito, este salga seco.	5	1
6	Tip extra: podés disfrutar este bizcochuelo solo o podés rellenarlo con dulce de leche o crema y te servirá como base para una torta de cumpleaños.  	6	1
7	Vamos a necesitar 60 gramos de mantequilla blanda	1	2
8	Añadimos el azúcar, (yo tengo 35 gramos)	2	2
9	Añadimos un sobre de azúcar de vainilla, si no tienes, puedes poner esencia de vainilla	3	2
10	Añadimos una pizca de sal y lo mezclamos	4	2
11	Añadimos la yema de un huevo y la integramos	5	2
12	Y añadimos la leche (yo tengo 80 ml de leche)	6	2
13	Añadimos 250 gr de harina de trigo y levadura química o polvos de hornear	7	2
14	Tamizamos la harina. Si no tienes tamiz pásalo por un colador	8	2
15	Batir a mano los huevos con el azúcar.	1	3
16	Incorporar el aceite y la ralladura y jugo de limón y seguir batiendo.	2	3
17	Agregar en varios pasos la harina tamizada y mezclar con movimientos envolventes.	3	3
18	Aceitar un molde y podés enharinarlo o mejor aún ponerle azúcar.	4	3
19	Picar las cebollas.	1	4
20	Cortar los tomates en cubitos.	2	4
21	Poner en un bowl la carne, los tomates y la cebolla y rociar con el jugo de los 5 limones.	3	4
22	Llevar a la heladera por 1 hora y media aproximadamente.	4	4
23	Formar bolitas y poner en el centro de la masa y doblar en triángulo.	5	4
24	Derretir la manteca agregar la cucharada de maicena revolver y cocinar un poquito agregar de golpe la taza de leche y revolver agregar sal pimienta y nuez moscada e ir batiendo hasta que espese.	1	5
25	Integrar los huevos con el azúcar y la leche.	1	6
26	Añadir la harina y mezclar. Dejar reposar 20 minutos en un lugar frío.	2	6
27	Sobre una sartén de teflón enmantecada o rociada con spray vegetal colocar un cucharón de masa formando una capa fina.	3	6
28	Cocinar de ambos lados.\nRellenar los panqueques con dulce de leche.	4	6
29	Salpimentar la colita de cuadril, cubrir con la mostaza y luego enharinar por completo la carne.	1	7
30	Colocar en una placa para horno, realizar unos cortes en la parte superior y ubicar trozos de manteca sobre la carne.	2	7
31	Llevar a horno precalentado a 180° hasta que quede bien dorada y cocida la carne.	3	7
32	Para la guarnición, cortar las papas en cuña, salpimentar y colocar en una placa para horno.	4	7
33	Agregar el romero fresco y llevar al horno hasta que estén crocantes y doradas.	5	7
34	En un recipiente pon la levadura. Añade el agua y remueve. El agua ha de estar a unos 28 - 30ºC. Es decir, un poquito más fría que la temperatura del cuerpo humano. Si tu harina tiene entre 11% y 12% de proteínas pon solo 300 g de agua. Si tiene mas de 12 % de proteínas pon 320 g de agua.	1	8
35	Tamiza la harina. Añade la sal. Con ayuda de una cuchara remueve muy bien.	2	8
36	Coge un recipiente y úntalo con pequeña cantidad de aceite. Pon dentro la masa. Cierra el recipiente y, directamente, guarda la masa en la nevera entre 12 y 14 horas. En verano ponla en la parte más fría de la nevera: en la balda que está más cerca del congelador. Y en invierno al contrario, en la balda que esta más alejada del congelador. 	3	8
37	Saca la masa de la nevera. Espolvorea la mesa con harina. Vuelca la masa sobre la mesa espolvoreada.	4	8
38	Estira la masa en una rectángulo de 20x25 cm. Manipúlala con cuidado y cariño, para no deshincharla mucho.	5	8
39	Por el lado más largo enrolla la masa. El rollo obtenido corta en dos.	6	8
40	Cierra las puntas.	7	8
41	Tapa las piezas obtenidas con una toalla y déjalas en reposo hasta que se hinchen. A 20 - 22ºC aproximadamente 1 hora.  A temperatura más alta un poco menos de tiempo y a temperatura mas baja un poco más.	8	8
42	Cuando falten 35 minutos para que termine el levado enciende el horno a 250ºC con calor sólo de abajo. Si no tienes esta función, pon el calor de arriba y abajo.	9	8
43	En el fondo del horno pon una bandeja para echar el agua.	10	8
44	Pon las piezas de masa sobre un papel para hornear y estíralas. Manipula la masa con cuidado y cariño, para no deshincharla mucho.	11	8
45	Mete el pan dentro del horno. Si no tienes una piedra para hornear, hornealo en una bandeja.	12	8
46	En la bandeja del fondo echa un vaso de agua hirviendo.	13	8
47	Hornea el stirato 10 - 12 minutos más o hasta que quede como a ti te gusta.	14	8
48	Picamos finamente una cebolla mediana.	1	9
49	Rallamos una zanahoria pequeña.	2	9
50	Cortamos en juliana un cuarto de pimiento morrón, aunque añadir pimiento es totalmente opcional.	3	9
51	En una sartén calentamos dos cucharadas de aceite añadimos la cebolla y la doramos.	4	9
52	Añadimos la zanahoria rallada y la rehogamos un par de minutos.	5	9
53	Añadimos la carne y la sofreímos hasta que cambie de color.	6	9
54	Añadimos el pimiento y lo rehogamos un par de minutos.	7	9
55	Colocamos por encima unos 180 o 200 gramos de nidos de pasta.	8	9
56	Cubrimos con 600 ml de zumo de tomate.	9	9
57	Tapamos y cocemos a fuego medio 10 minutos.	10	9
58	Le damos la vuelta a la pasta y la cocemos bien tapadita y a fuego medio 5 minutos más o hasta que quede como a ti te gusta.	11	9
59	Salpimentamos y añadimos un poco de orégano, albahaca o las especias que más te gusten.	12	9
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password, profile_image) FROM stdin;
1	agustincomolli	agustincomolli@yahoo.com.ar	scrypt:32768:8:1$lnoL6VM7JPzVZSy0$802a379b9d8b824d407af09f6789b21a18b1b1cbc87955d63c4425bebb921562d5e09ba112be90965352d8d6dd3c41a38866b6b03c2fa54217f9fc2e07cc4738	\\x5249464682753030313575303030307530303030574542505650382082753030313575303030307530303030826775303030308275303030312a
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 5, true);


--
-- Name: ingredients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingredients_id_seq', 1, false);


--
-- Name: recipes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.recipes_id_seq', 1, false);


--
-- Name: steps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.steps_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- Name: steps steps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ingredients ingredients_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: recipes recipes_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: recipes recipes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: steps steps_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- PostgreSQL database dump complete
--

