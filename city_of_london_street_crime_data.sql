SELECT SUBSTRING(`city_of_london_street_crime_data`.`Crime type`, 1, 1024) AS `Crime type`,
  SUBSTRING(`city_of_london_street_crime_data`.`Last Outcome`, 1, 1024) AS `Last Outcome`,
  SUBSTRING(`city_of_london_street_crime_data`.`context`, 1, 1024) AS `context`,
  SUBSTRING(`city_of_london_street_crime_data`.`date`, 1, 1024) AS `date`,
  `city_of_london_street_crime_data`.`id` AS `id`,
  SUBSTRING(`city_of_london_street_crime_data`.`latitude`, 1, 1024) AS `latitude`,
  SUBSTRING(`city_of_london_street_crime_data`.`location_subtype`, 1, 1024) AS `location_subtype`,
  SUBSTRING(`city_of_london_street_crime_data`.`location_type`, 1, 1024) AS `location_type`,
  SUBSTRING(`city_of_london_street_crime_data`.`longitude`, 1, 1024) AS `longitude`,
  `city_of_london_street_crime_data`.`month` AS `month`,
  SUBSTRING(`city_of_london_street_crime_data`.`name`, 1, 1024) AS `name`,
  SUBSTRING(`city_of_london_street_crime_data`.`persistent_id`, 1, 1024) AS `persistent_id`,
  `city_of_london_street_crime_data`.`street` AS `street`
FROM `city_of_london_street_crime_data`