use sakila;
#1a. Display the first and last names of all actors from the table actor.
select first_name, last_name from actor;
#1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
select concat(first_name, " ", last_name) as actor_name from actor;
#2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select actor_id, first_name, last_name from actor where first_name='JOE';
#2b. Find all actors whose last name contain the letters GEN:
select * from actor where last_name like '%G%' and last_name like '%E%' and last_name like '%N%';
#2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
select * from actor where last_name like '%l%' and last_name like '%I%' order by last_name, first_name;
#2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country from country where country in ('Afghanistan', 'Bangladesh', 'China');
#3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
ALTER TABLE `sakila`.`actor` 
ADD COLUMN `description` BLOB NULL AFTER `last_update`;
#3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE `sakila`.`actor` 
DROP COLUMN `description`;
#4a. List the last names of actors, as well as how many actors have that last name.
select distinct last_name, count(last_name) from actor group by last_name;
#4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select distinct last_name, count(last_name) from actor group by last_name having count(last_name) >= 2;
#4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
UPDATE actor
SET  first_name= 'HARPO', last_name= 'WILLIAMS'
WHERE first_name = 'GROUCHO' and last_name = 'WILLIAMS';
#4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
SET SQL_SAFE_UPDATES = 1;

UPDATE actor
SET first_name = 'GROUCHO'
WHERE first_name = 'HARPO';
#5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
show create table address;
#6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
select staff.first_name, staff.last_name, address.address
from staff
left join address on staff.address_id = address.address_id;
#6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
select staff.staff_id, staff.first_name, staff.last_name, sum(payment.amount)
from staff
left join payment on staff.staff_id = payment.staff_id
group by staff.staff_id;
#6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
select film.title, count(film_actor.actor_id) as num_of_actors
from film
inner join film_actor on film_actor.film_id = film.film_id
group by film_actor.film_id;
#6d. How many copies of the film Hunchback Impossible exist in the inventory system?
select inventory.film_id, count(inventory.film_id) as copies from inventory
where inventory.film_id in (select film.film_id from film where film.title = 'Hunchback Impossible')
group by inventory.film_id;
#6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
select customer.first_name, customer.last_name, sum(payment.amount)
from customer
inner join payment on payment.customer_id = customer.customer_id
group by payment.customer_id
order by customer.last_name;
#7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
select film.title from film
where language_id = 1 and film.title like 'K%' or film.title like 'Q%';
#7b. Use subqueries to display all actors who appear in the film Alone Trip.
select actor.first_name, actor.last_name from actor
where actor.actor_id in (
	select film_actor.actor_id from film_actor
	where film_id in (
		select film.film_id from film where film.title = 'Alone Trip'
	)
);
#7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
select customer.first_name, customer.last_name, customer.email
from customer
where customer.address_id in (
	select address.address_id from address where address.city_id in (
		select city_id from city where country_id in (
			select country_id from country where country = 'Canada'
		)
	)
);
#7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
select * from film where rating = 'G';
#7e. Display the most frequently rented movies in descending order.
CREATE VIEW frequency as
SELECT rental.rental_id, inventory.film_id
FROM rental
left join inventory on rental.inventory_id = inventory.inventory_id;

select film.title, count(frequency.film_id) as most_rented_movies
from film
inner join frequency on film.film_id = frequency.film_id
group by frequency.film_id
order by most_rented_movies desc;
#7f. Write a query to display how much business, in dollars, each store brought in.
select staff_id as store_id, sum(amount)
from payment
group by staff_id;
#7g. Write a query to display for each store its store ID, city, and country.
create view store_city as
select store.store_id, address.city_id
from store
left join address on store.address_id = address.address_id;

create view store_country as
select store_city.store_id, city.city, city.country_id
from store_city
left join city on store_city.city_id = city.city_id;

select * from store_country;

select store_country.store_id,store_country.city,country.country
from store_country
left join country on store_country.country_id = country.country_id;
#7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
#8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
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
#8b. How would you display the view that you created in 8a?
select * from top_5_gross_rev;
#8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view top_5_gross_rev;

