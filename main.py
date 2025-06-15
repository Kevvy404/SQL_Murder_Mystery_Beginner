import sqlite3

def execute_and_print(cursor, query, description):
    print(f"\n=== {description} ===")
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    return results

def solve_mystery():
    # Connect to database
    conn = sqlite3.connect('sql-murder-mystery.db')
    cursor = conn.cursor()
    
    try:
        # 1. Find the murder crime scene report
        execute_and_print(cursor,
            """SELECT * FROM crime_scene_report 
               WHERE type = 'murder' 
               AND city = 'SQL City' 
               AND date = '20180115'""",
            "Murder Crime Scene Report"
        )
        
        # 2. Find the witness who lives at the last house
        execute_and_print(cursor,
            """SELECT * FROM person 
               WHERE address_number = (
                   SELECT MAX(address_number) FROM person
               )""",
            "Witness at Last House"
        )
        
        # 3. Find Annabel's information
        execute_and_print(cursor,
            """SELECT * FROM person 
               WHERE name LIKE 'Annabel %' 
               AND address_street_name = 'Franklin Ave'""",
            "Annabel's Information"
        )
        
        # 4. Get witness interviews
        execute_and_print(cursor,
            "SELECT * FROM interview WHERE person_id = '16371'",
            "First Witness Interview (Morty)"
        )
        
        execute_and_print(cursor,
            "SELECT * FROM interview WHERE person_id = '14887'",
            "Second Witness Interview (Annabel)"
        )
        
        # 5. Investigate gym check-ins
        execute_and_print(cursor,
            """SELECT * FROM get_fit_now_check_in 
               WHERE check_in_date = '20180109' 
               AND membership_id LIKE '48Z%'""",
            "Gym Check-ins on Jan 9"
        )
        
        # 6. Get gym member details
        execute_and_print(cursor,
            """SELECT * FROM get_fit_now_member 
               WHERE id IN ('48Z55', '49Z7A') 
               AND membership_status = 'gold'""",
            "Gold Gym Members"
        )
        # 7. Caught the Murder!
        execute_and_print(cursor,
            "SELECT * FROM person WHERE id = '67318'",
            "MURDER"
        )
        
        # 8. Get suspect interview
        execute_and_print(cursor,
            "SELECT * FROM interview WHERE person_id = '67318'",
            "Suspect Interview (Jeremy Bowers)"
        )
        
        # 9. Find mastermind's car details
        execute_and_print(cursor,
            """SELECT * FROM drivers_license 
               WHERE gender = 'female' 
               AND height BETWEEN 65 AND 67 
               AND hair_color = 'red' 
               AND car_make = 'Tesla' 
               AND car_model = 'Model S'""",
            "Mastermind's Car Details"
        )
        
        # 10. Find person IDs from license IDs
        execute_and_print(cursor,
            """SELECT * FROM person 
               WHERE license_id IN ('202298', '291182', '918773')""",
            "Potential Masterminds"
        )
        
        # 11. Check income of suspects
        execute_and_print(cursor,
            """SELECT * FROM income 
               WHERE ssn IN ('961388910', '337169072', '987756388')""",
            "Suspects' Income"
        )
        
        # 12. Verify concert attendance
        execute_and_print(cursor,
            """SELECT * FROM facebook_event_checkin 
               WHERE person_id = '99716' 
               AND event_name = 'SQL Symphony Concert' 
               AND date BETWEEN '20170101' AND '20171231'""",
            "Concert Attendance"
        )
        
        # Final verification
        execute_and_print(cursor,
            """SELECT p.name, COUNT(*) as concert_count 
               FROM facebook_event_checkin f
               JOIN person p ON f.person_id = p.id
               WHERE f.event_name = 'SQL Symphony Concert' 
               AND f.date BETWEEN '20170101' AND '20171231'
               AND p.id = '99716'
               GROUP BY p.name
               HAVING COUNT(*) = 3""",
            "Final Verification"
        )
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    solve_mystery()