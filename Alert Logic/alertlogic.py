# *Nix Python Path

import boto3
import requests
import json

AlApiHostsUrl = ''
AlApiProtectedHostsUrl = ''
AlApiKey = ''

AlHostsRequest = requests.get( AlApiHostsUrl, auth=( AlApiKey,'' ) )
AlProtectedHostsRequest = requests.get( AlApiProtectedHostsUrl, auth=( AlApiKey,'' ) )

AlHostsStack = json.loads( AlHostsRequest.text )
AlProtectedHostsStack = json.loads( AlProtectedHostsRequest.text )

AlHosts = {}
AlOfflineHosts = {}
AlOnlineHosts = {}

AlProtectedHosts = {}
AlOfflineProtectedHosts = {}
AlOnlineProtectedHosts = {}

AwsEc2InstancesTag = {}

AlAwsHosts = {}

def GetAwsEc2Regions():
    
    count = 1

    AwsSessionRegions = boto3.session.Session()
    AwsEc2Regions = AwsSessionRegions.get_available_regions( 'ec2' )

    for region in AwsEc2Regions:
    
        # AWS credintials
        session = boto3.session.Session(
            aws_access_key_id = '',
            aws_secret_access_key = '',
            region_name = region
        )    

        AwsEc2Client = session.client('ec2')
        AwsEc2Tags = AwsEc2Client.describe_tags()
        
        print " %d. ScanningRegion: %s " % ( count, region )
        
        count += 1
        
        SetAwsEc2InstancesTag( AwsEc2Tags )
             
def SetAwsEc2InstancesTag( AwsEc2Tags ):
    
    for tag in AwsEc2Tags['Tags']:
        
        if ( tag[ 'ResourceType' ] == 'instance' and tag[ 'Key' ] == 'Name' ):
            
            AwsEc2InstancesTag.update( { tag[ 'ResourceId' ]: tag[ 'Value' ] } )

def GetAwsEc2InstancesTag():
    
    count = 1
    
    for instance in AwsEc2InstancesTag:
          
        print " %d. Instance: %s InstanceTag: %s " % ( count, instance, AwsEc2InstancesTag[ instance ] )
        
        count += 1

def SetAlOfflineHosts( HostName, HostStatus, HostId ):
        
    if ( HostStatus == 'offline' ):
                
        AlOfflineHosts.update( { HostName: HostId } )
                
def SetAlOnlineHosts( HostName, HostStatus, HostId ):
        
    if ( HostStatus == 'ok' ):
                
        AlOnlineHosts.update( { HostName: HostId } )
                
def SetAlHosts( HostName, HostStatus, HostId ):
        
    AlHosts.update( { HostName: [ HostId, HostStatus ] } )
    
def GetAlHostsStatus():

    count = 1
        
    for host in AlHostsStack[ 'hosts' ]:
        
        if ( host[ 'host' ][ 'type' ] == 'host' ):
            
            HostName = host[ 'host' ][ 'name' ]
            HostId = host[ 'host' ][ 'id' ]
            HostStatus = host[ 'host' ][ 'status' ][ 'status' ]
    
            print " %d. HostName: %s, HostId: %s, HostStatus: %s " % ( count, HostName, HostId, HostStatus )
            
            count += 1
                
            SetAlHosts( HostName, HostStatus, HostId )
            SetAlOfflineHosts( HostName, HostStatus, HostId )
            SetAlOnlineHosts( HostName, HostStatus, HostId )
                
def GetAlOnlineHosts():
        
    count = 1
    
    for host in AlOnlineHosts:
    
        print " %d. Online Host: %s HostId: %s " % ( count, host, AlOnlineHosts[ host ] )
        
        count += 1
        
def GetAlOfflineHosts():
        
    count = 1
    
    for host in AlOfflineHosts:   
        
        print " %d. Offline Host: %s HostId: %s " % ( count, host, AlOfflineHosts[ host ] )
        
        count += 1
                
def GetAlHosts():
        
    count = 1
        
    for host in AlHosts:
                
        print " %d. Host: %s HostId: %s HostStatus: %s " % ( count, host, AlHosts[ host ][ 0 ], AlHosts[ host ][ 1 ] )
                
        count += 1

def SetAlOfflineProtectedHosts( ProtectedHostName, ProtectedHostStatus, ProtectedHostId ):
        
    if ( ProtectedHostStatus == 'offline' ):
                
        AlOfflineProtectedHosts.update( { ProtectedHostName: ProtectedHostId } )
                
def SetAlOnlineProtectedHosts( ProtectedHostName, ProtectedHostStatus, ProtectedHostId ):
        
    if ( ProtectedHostStatus == 'ok' ) or ( ProtectedHostStatus == 'new' ):
                
        AlOnlineProtectedHosts.update( { ProtectedHostName: ProtectedHostId } )
                
def SetAlProtectedHosts( ProtectedHostName, ProtectedHostStatus, ProtectedHostId ):
        
    AlProtectedHosts.update( { ProtectedHostName: [ ProtectedHostId, ProtectedHostStatus ] } )
                
def GetAlProtectedHostsStatus():

    count = 1
        
    for ProtectedHost in AlProtectedHostsStack[ 'protectedhosts' ]:
        
        if ( ProtectedHost[ 'protectedhost' ][ 'type' ] == 'host' ):
            
            ProtectedHostName = ProtectedHost[ 'protectedhost' ][ 'name' ]
            ProtectedHostId = ProtectedHost[ 'protectedhost' ][ 'id' ]
            ProtectedHostStatus = ProtectedHost[ 'protectedhost' ][ 'status' ][ 'status' ]
    
            print " %d. ProtectedHostName: %s, ProtectedHostId: %s, ProtectedHostStatus: %s " % ( count, ProtectedHostName, ProtectedHostId, ProtectedHostStatus )
            
            count += 1
                
            SetAlProtectedHosts( ProtectedHostName, ProtectedHostStatus, ProtectedHostId )
            SetAlOfflineProtectedHosts( ProtectedHostName, ProtectedHostStatus, ProtectedHostId )
            SetAlOnlineProtectedHosts( ProtectedHostName, ProtectedHostStatus, ProtectedHostId )

def GetAlOnlineProtectedHosts():
        
    count = 1
    
    for ProtectedHost in AlOnlineProtectedHosts:
    
        print " %d. Online ProtectedHost: %s ProtectedHostId: %s " % ( count, ProtectedHost, AlOnlineProtectedHosts[ ProtectedHost ] )
        
        count += 1
        
def GetAlOfflineProtectedHosts():
        
    count = 1
    
    for ProtectedHost in AlOfflineProtectedHosts:   
        
        print " %d. Offline ProtectedHost: %s ProtectedHostId: %s " % ( count, ProtectedHost, AlOfflineProtectedHosts[ ProtectedHost ] )
        
        count += 1
                
def GetAlProtectedHosts():
        
    count = 1
        
    for ProtectedHost in AlProtectedHosts:
                
        print " %d. ProtectedHost: %s ProtectedHostId: %s ProtectedHostStatus: %s " % ( count, ProtectedHost, AlProtectedHosts[ ProtectedHost ][ 0 ], AlProtectedHosts[ ProtectedHost ][ 1 ] )
    
        count += 1
                
def DeleteAlOfflineHosts():
        
    count = 1
        
    for host in AlOfflineHosts:
                
        DeleteAlApiHostUrl = AlApiHostsUrl + '/' + AlOfflineHosts[ host ] 
                
        requests.delete( DeleteAlApiHostUrl, auth=( AlApiKey,'' ) )
                
        print " %d. Offline Host: %s HostId: %s has been deleted " % ( count, host, AlOfflineHosts[ host ] )
                
        count += 1
                
def DeleteAlOfflineProtectedHosts():
        
    count = 1
        
    for ProtectedHost in AlOfflineProtectedHosts:
                
        DeleteAlApiProtectedHostUrl = AlApiProtectedHostsUrl + '/' + AlOfflineProtectedHosts[ ProtectedHost ] 
                
        requests.delete( DeleteAlApiProtectedHostUrl, auth=( AlApiKey,'' ) )
                
        print " %d. Offline ProtectedHost: %s ProtectedHostId: %s has been deleted " % ( count, ProtectedHost, AlOfflineProtectedHosts[ ProtectedHost ] )
                
        count += 1
        
def GetAlAwsHostsMatch():
    
    count = 1
    
    for host in AlProtectedHosts:
        
        for instance in AwsEc2InstancesTag:
            
            if ( host == instance ):
                
                ProtectedHostTag = AwsEc2InstancesTag[ instance ]
                ProtectedHostId = AlProtectedHosts[ host ][ 0 ]
                
                print " %d. ProtectedHostMatched: %s ProtectedHostTag: %s ProtectedHostId: %s" % ( count, host, ProtectedHostTag, ProtectedHostId )
                
                count += 1
                
                SetAlAwsHosts( host, ProtectedHostTag, ProtectedHostId )
                
def SetAlAwsHosts( host, ProtectedHostTag, ProtectedHostId ):
    
    AlAwsHosts.update( { host: [ ProtectedHostTag, ProtectedHostId ] } )
    
def GetAlAwsHosts():
    
    count = 1
    
    for host in AlAwsHosts:
        
        print " %d. ProtectedHost: %s ProtectedHostTag: %s ProtectedHostId: %s" % ( count, host, AlAwsHosts[ host ][ 0 ], AlAwsHosts[ host ][ 1 ] )
        
        count += 1
        
def SetAlHostsTag():
    
    count = 1
    
    for host in AlAwsHosts:
        
        data = { "protectedhost": { "name": host, "tags": [ { "name": AlAwsHosts[ host ][ 0 ] } ] } }
        
        AlHostDataTag = json.dumps( data )
        
        UpdateAlApiTagUrl = AlApiProtectedHostsUrl + '/' + AlAwsHosts[ host ][ 1 ]
        
        requests.post( UpdateAlApiTagUrl, AlHostDataTag, auth=( AlApiKey,'' ) )
        
        print " %d. ProtectedHost: %s ProtectedHostTag: %s has been set " % ( count, host, AlAwsHosts[ host ][ 0 ] )
        
        count += 1
                
if __name__ == "__main__":

#----Hosts Funtions------------------
        
#    GetAlHostsStatus()
#    GetAlOnlineHosts()
#    GetAlOfflineHosts()
#    GetAlHosts()
#    DeleteAlOfflineHosts()

#----Protected Hosts Funtions--------
        
#    GetAlProtectedHostsStatus()
#    GetAlOnlineProtectedHosts()
#    GetAlOfflineProtectedHosts()
#    GetAlProtectedHosts()
#    DeleteAlOfflineProtectedHosts()
        
#----AWS Get Instances Tag Functions---
        
#    GetAwsEc2Regions()
#    GetAwsEc2InstancesTag()

#----Match AL and AWS Hosts------------ 
 
#    GetAlAwsHostsMatch()
#    GetAlAwsHosts()

#----Set AL Tags-----------------------

#    SetAlHostsTag()

#----Deleting Hosts And Setting The Tags Job-------- 
    
    GetAlProtectedHostsStatus()
    print '---------------------------'
    DeleteAlOfflineProtectedHosts()
    print '---------------------------'
    GetAlHostsStatus()
    print '---------------------------'
    DeleteAlOfflineHosts()
    print '---------------------------'
    GetAwsEc2Regions()
    print '---------------------------'
    GetAlAwsHostsMatch()
    print '---------------------------'
    SetAlHostsTag()