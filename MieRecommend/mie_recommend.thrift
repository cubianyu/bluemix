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
  1: i64 business_id,
  2: string name,
  3: string photo_url,
  4: string telephone
  5: string address,
  6: double longitude,
  7: double latitude,
  8: i32 distance,
  9: i32 avg_price
  10: double recommend_mark,
  11: list<string> recommend_reason,
  12: list<Dish> favourite_dishes,
  13: list<GroupOn> deals
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