from snowflake import SnowflakeGenerator

gen = SnowflakeGenerator(1)


def get_snow_id():
    return next(gen)

if __name__ == '__main__':
    print(get_snow_id())
