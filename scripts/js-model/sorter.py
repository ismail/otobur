import otobur_pb2
import sys

if __name__ == "__main__":
    schedule = otobur_pb2.Schedule()
    schedule.ParseFromString(open(sys.argv[1],"rb").read())
    for line in schedule.lines:
        print("####################################")
        for stop in line.stops:
            print("%d - %d (%s %s)" % (stop.order, stop.direction, stop.name, line.name))
        print("####################################")

