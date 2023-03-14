import argparse
import logging
from pvsimulator.meter import Meter
from pvsimulator.simulator import Simulator


def start_meter(args):
    meter = Meter(args.broker, args.port, args.queue, args.username, args.password)
    meter.start()


def start_simulator(args):
    simulator = Simulator(args.broker, args.port, args.queue, args.username, args.password, args.outfile)
    simulator.start()


def main():

    root_logger = logging.getLogger("pvsimulator")
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(name)s:%(created)f:%(message)s")
    shandler = logging.StreamHandler()
    shandler.setFormatter(formatter)
    root_logger.addHandler(shandler)

    parser = argparse.ArgumentParser(description="Photovoltaic simulator")
    
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommads",
        help="sub-command help")

    parser_meter = subparsers.add_parser("start-meter", help="Starting meter producer...")
    parser_meter.add_argument("-b", "--broker", type=str, required=True, help="Broker URL")
    parser_meter.add_argument("-p", "--port", type=int, required=True, help="Broker port")
    parser_meter.add_argument("-q", "--queue", type=str, required=True, help="Broker queue")
    parser_meter.add_argument("-u", "--username", type=str, required=True, help="UserName")
    parser_meter.add_argument("-x", "--password", type=str, required=True, help="Password")
    parser_meter.set_defaults(func=start_meter)

    parser_simulator = subparsers.add_parser("start-simulator", help="Starting PV simulator consumer...")
    parser_simulator.add_argument("-b", "--broker", type=str, required=True, help="Broker URL")
    parser_simulator.add_argument("-p", "--port", type=int, required=True, help="Broker port")
    parser_simulator.add_argument("-q", "--queue", type=str, required=True, help="Broker queue")
    parser_simulator.add_argument("-u", "--username", type=str, required=True, help="UserName")
    parser_simulator.add_argument("-x", "--password", type=str, required=True, help="Password")
    parser_simulator.add_argument("-o", "--outfile", default="pv-simulator-output.csv", help="Output file path")
    parser_simulator.set_defaults(func=start_simulator)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
