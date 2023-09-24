# Create a cursor object
import database_connector


def getProfiles():
    cursor = database_connector.db.cursor()

    cursor.execute("SELECT * FROM profile")

    result = cursor.fetchall()

    column_names = [i[0] for i in cursor.description]

    json_result = []

    for row in result:
        obj = {}
        for i in range(len(column_names)):
            obj[column_names[i]] = row[i]
        json_result.append(obj)

    cursor.execute("select * from cached_stat limit 0")
    cursor.fetchall()

    column_names = [i[0] for i in cursor.description]

    for profile in json_result:
        cursor.execute(f'SELECT * FROM cached_stat WHERE id = {profile["cached_stat"]}')
        stat = cursor.fetchall()[0]

        obj = {}
        for i in range(len(column_names)):
            obj[column_names[i]] = stat[i]
        profile["cached_stat"] = obj

        # delete unnecessary fields and reformat
        del profile['forms_before_ad']
        del profile['cached_stat']['profile_card']
        del profile['cached_stat']['detailed_stat']
        profile['active'] = profile['active'] == 1
        profile['banned'] = profile['banned'] == 1
        profile['global_search'] = profile['global_search'] == 1

    cursor.close()

    return json_result
