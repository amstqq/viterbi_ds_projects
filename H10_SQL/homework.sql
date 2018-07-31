use sakila;

select first_name, last_name from actor;

select concat(first_name, " ", last_name) as actor_name from actor;

select actor_id, first_name, last_name from actor where first_name='JOE';

select * from actor where last_name like '%G%' and last_name like '%E%' and last_name like '%N%';

select * from actor where last_name like '%l%' and last_name like '%I%' order by last_name, first_name;

select country_id, country from country where country in ('Afghanistan', 'Bangladesh', 'China');

ALTER TABLE `sakila`.`actor` 
ADD COLUMN `description` BLOB NULL AFTER `last_update`;

ALTER TABLE `sakila`.`actor` 
DROP COLUMN `description`;

select distinct last_name, count(last_name) from actor group by last_name;

select distinct last_name, count(last_name) from actor group by last_name having count(last_name) >= 2;

UPDATE actor
SET  first_name= 'HARPO', last_name= 'WILLIAMS'
WHERE first_name = 'GROUCHO' and last_name = 'WILLIAMS';

SET SQL_SAFE_UPDATES = 1;

UPDATE actor
SET first_name = 'GROUCHO'
WHERE first_name = 'HARPO';

show create table address;

select staff.first_name, staff.last_name, address.address
from staff
left join address on staff.address_id = address.address_id;

select staff.staff_id, staff.first_name, staff.last_name, sum(payment.amount)
from staff
left join payment on staff.staff_id = payment.staff_id
group by staff.staff_id;

select film.title, count(film_actor.actor_id) as num_of_actors
from film
inner join film_actor on film_actor.film_id = film.film_id
group by film_actor.film_id;

select inventory.film_id, count(inventory.film_id) as copies from inventory
where inventory.film_id in (select film.film_id from film where film.title = 'Hunchback Impossible')
group by inventory.film_id;

select customer.first_name, customer.last_name, sum(payment.amount)
from customer
inner join payment on payment.customer_id = customer.customer_id
group by payment.customer_id
order by customer.last_name;

select film.title from film
where language_id = 1 and film.title like 'K%' or film.title like 'Q%';

select actor.first_name, actor.last_name from actor
where actor.actor_id in (
	select film_actor.actor_id from film_actor
	where film_id in (
		select film.film_id from film where film.title = 'Alone Trip'
	)
);

select customer.first_name, customer.last_name, customer.email
from customer
where customer.address_id in (
	select address.address_id from address where address.city_id in (
		select city_id from city where country_id in (
			select country_id from country where country = 'Canada'
		)
	)
);

select * from film where rating = 'G';

CREATE VIEW frequency as
SELECT rental.rental_id, inventory.film_id
FROM rental
left join inventory on rental.inventory_id = inventory.inventory_id;

select film.title, count(frequency.film_id) as most_rented_movies
from film
inner join frequency on film.film_id = frequency.film_id
group by frequency.film_id
order by most_rented_movies desc;

select staff_id as store_id, sum(amount)
from payment
group by staff_id;

create view store_city as
select store.store_id, address.city_id
from store
left join address on store.address_id = address.address_id;

select * from store_city;

create view store_country as
select store_city.store_id, city.city, city.country_id
from store_city
left join city on store_city.city_id = city.city_id;

select * from store_country;

select store_country.store_id,store_country.city,country.country
from store_country
left join country on store_country.country_id = country.country_id;

create view temp as
select payment.rental_id, payment.amount, rental.inventory_id
from payment
left join rental on payment.rental_id = rental.rental_id;

create view temp2 as
select temp.amount, inventory.film_id
from temp
left join inventory on temp.inventory_id = inventory.inventory_id;

create view temp3 as
select film_category.category_id, temp2.amount
from temp2
left join film_category on film_category.film_id = temp2.film_id;

create view top_5_gross_rev as
select category.`name`, sum(temp3.amount) as gross_revenue
from temp3
left join category on temp3.category_id = category.category_id
group by category.`name`
order by gross_revenue desc
limit 5;

select * from top_5_gross_rev;

drop view top_5_gross_rev;

