namespace py mie_recommend

struct Dish {
  1: i64 id,
  2: string name,
  3: i32 price
}

struct GroupOn {
  1: string type,
  2: string name,
  3: double price,
  4: string url
}

struct Recommend {
  1: i64 id,
  2: i64 dp_business_id,
  3: string name,
  4: string pic_url,
  5: i32 average_cost,
  6: string address,
  7: list<string> tels,
  8: double longitude,
  9: double latitude,
  10: i32 distance,
  11: double recommend_mark,
  12: list<string> recommend_reason,
  13: list<Dish> favourite_dishes,
  14: list<GroupOn> groupon
}

struct GeoInfo{
  1: string city,
  2: string district,
  3: double longitude,
  4: double latitude
}

struct Mode{
  1: i32 number,
  2: i32 type,
  3: i64 style
}

service RecommendService {
  list<Recommend> recommend(1:i64 user_id, 2:GeoInfo geo_info, 3:Mode mode)
}