#회사명 추출해서 중복 제거 후 DB 저장하기

from mongo import MongoDB
db = MongoDB()

result = db.selectDistinct("job_comp")

print(result)
