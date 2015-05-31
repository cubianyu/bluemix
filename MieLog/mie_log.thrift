namespace py mie_log

enum mie_log_type {
  RECOMMEND = 0,
  VIEW = 1,
  REJECT = 2,
  ACCEPT = 3,
  FAVORITE = 4,
  VISIT = 5
  PRICING = 6
}

struct mie_log_struct {
  1: i64 business_id
  2: mie_log_type type
  3: double mark
}

service LogCollectService {
  i32 collect(1: list<mie_log_struct> logs)
}