#include "ns3/command-line.h"
#include "ns3/constant-position-mobility-model.h"
#include "ns3/end-device-lora-phy.h"
#include "ns3/end-device-lorawan-mac.h"
#include "ns3/gateway-lora-phy.h"
#include "ns3/gateway-lorawan-mac.h"
#include "ns3/log.h"
#include "ns3/lora-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/node-container.h"
#include "ns3/forwarder-helper.h"
#include "ns3/periodic-sender-helper.h"
#include "ns3/position-allocator.h"
#include "ns3/simulator.h"
#include "ns3/ns2-mobility-helper.h"
#include "ns3/command-line.h"
#include "ns3/callback.h"
#include "ns3/config.h"
#include <algorithm>
#include <ctime>
#include <fstream>

using namespace ns3;
using namespace lorawan;

// Network settings
int nGateway = 1;
int nDevices = 193;
int appPeriodSeconds = 100;                   //!< Number of end device nodes to create
double simulationTimeSeconds = 5999.0; //!< Scenario duration (s) in simulated time
std::string ns2MobilityTraceFile = "/home/metehan/ns2mobility.tcl"; // Specify the NS-2 mobility trace file
std::string OutputFolder;


NS_LOG_COMPONENT_DEFINE("SimpleLorawanNetworkExample");


int
main(int argc, char* argv[])
{
    // Parse command line attribute
    CommandLine cmd(__FILE__);
    cmd.AddValue("nDevices", "Number of endDevices", nDevices);
    cmd.AddValue("period", "Duration of Simulation", appPeriodSeconds);
    cmd.AddValue("OutputFolder", "Log file", OutputFolder);
    cmd.Parse(argc, argv);


    //LogComponentEnable("SimpleLorawanNetworkExample", LOG_LEVEL_ALL);
    //LogComponentEnable("Ns2MobilityHelper", LOG_LEVEL_ALL);

    /************************
     *  Create the channel  *
     ************************/

    NS_LOG_INFO("Creating the channel...");

    // Create the lora channel object
    Ptr<LogDistancePropagationLossModel> loss = CreateObject<LogDistancePropagationLossModel>();
    loss->SetPathLossExponent(3.76);
    loss->SetReference(1, 7.7);

    Ptr<PropagationDelayModel> delay = CreateObject<ConstantSpeedPropagationDelayModel>();
    Ptr<LoraChannel> channel = CreateObject<LoraChannel>(loss, delay);

    /************************
     *  Create the helpers  *
     ************************/

    NS_LOG_INFO("Setting up helpers...");

    // Assign the NS-2 mobility model to the end devices
    Ns2MobilityHelper ns2Mobility = Ns2MobilityHelper(ns2MobilityTraceFile);

    MobilityHelper mobility;
    Ptr<ListPositionAllocator> allocator = CreateObject<ListPositionAllocator>();
    allocator->Add(Vector(0.0, 0.0, 15.0));      // Gateway position
    mobility.SetPositionAllocator(allocator);
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");

    // Create the LoraPhyHelper
    LoraPhyHelper phyHelper = LoraPhyHelper();
    phyHelper.SetChannel(channel);

    // Create the LorawanMacHelper
    LorawanMacHelper macHelper = LorawanMacHelper();

    // Create the LoraHelper
    LoraHelper helper = LoraHelper();
    helper.EnablePacketTracking(); // Ensure packet tracking is enabled

    /************************
     *  Create End Devices  *
     ************************/

    NS_LOG_INFO("Creating the end device...");

    // Create a set of nodes
    NodeContainer endDevices;
    endDevices.Create(nDevices);
    ns2Mobility.Install();


    // Create the LoraNetDevices of the end devices
    phyHelper.SetDeviceType(LoraPhyHelper::ED);
    macHelper.SetDeviceType(LorawanMacHelper::ED_A);
    helper.Install(phyHelper, macHelper, endDevices);
    

    /*********************
     *  Create Gateways  *
     *********************/

    NS_LOG_INFO("Creating the gateway...");
    
    NodeContainer gateways;
    gateways.Create(nGateway);

    // Make it so that nodes are at a certain height > 0
    mobility.SetPositionAllocator(allocator);
    mobility.Install(gateways);

    // Create a netdevice for each gateway
    phyHelper.SetDeviceType(LoraPhyHelper::GW);
    macHelper.SetDeviceType(LorawanMacHelper::GW);
    helper.Install(phyHelper, macHelper, gateways);

    /*********************************************
     *  Install applications on the end devices  *
     *********************************************/

    // Install applications in end devices
    PeriodicSenderHelper appHelper = PeriodicSenderHelper();
    appHelper.SetPeriod(Seconds(appPeriodSeconds));
    ApplicationContainer appContainer = appHelper.Install(endDevices);

    /******************
     * Set Data Rates *
     ******************/
    std::vector<int> sfQuantity(6);
    sfQuantity = LorawanMacHelper::SetSpreadingFactorsUp(endDevices, gateways, channel);


    std::cout << "Results for period= " << appPeriodSeconds << " end devices= " << nDevices << std::endl;
   
     // Activate printing of end device MAC parameters
    Time stateSamplePeriod = Seconds(simulationTimeSeconds);
    helper.EnablePeriodicDeviceStatusPrinting(endDevices, gateways, "/home/metehan/nodeData.txt", stateSamplePeriod);
    helper.EnablePeriodicPhyPerformancePrinting(gateways, "/home/metehan/phyPerformance.txt", stateSamplePeriod);
    /* PDR ve Delay hesapları için EnablePeriodicGlobalPerformancePrinting fonksiyonunda kullanılan “CountMacPacketsGlobally"
    fonksiyonu (lora-packet-tracker.cc) içerisinde düzenlenmiştir.*/
    helper.EnablePeriodicGlobalPerformancePrinting("/home/metehan/globalPerformance.txt", stateSamplePeriod);

    LoraPacketTracker& tracker = helper.GetPacketTracker();
    /****************
     *  Simulation  *
     ****************/

    Simulator::Stop(Seconds(simulationTimeSeconds));
    
    Simulator::Run();

    Simulator::Destroy();

    return 0;
}
