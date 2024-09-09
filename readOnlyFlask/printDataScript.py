from website.models import PastInput

print("My shell script is running")
records=PastInput.query.all()
for record in records:
    print(record.id,record.pastInput)