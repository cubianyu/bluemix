namespace py mie_log

enum LogType {
  RECOMMEND = 0,
  VIEW = 1,
  REJECT = 2,
  ACCEPT = 3,
  FAVORITE = 4,
  VISIT = 5
  PRICING = 6
}

struct Log {
  1: i64 business_id
  2: i64 user_id
  3: LogType type
  4: double mark
  5: i64 timestamp
}

service LogCollectService {
  i32 collect(1: list<Log> logs)
}