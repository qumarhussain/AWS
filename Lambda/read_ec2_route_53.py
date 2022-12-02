import boto3

def get_list_ec2_instances_tags():
    ec2 = boto3.resource('ec2')
    ids= [instance.id for instance in ec2.instances.all()]
    
    all_tags = []
    for i in ec2.instances.all():
        for idx, tag in enumerate(i.tags):
            all_tags.append(tag['Value'])
    
    return all_tags

def get_list_hosted_zone(all_tags,routes):
    
    response = routes.list_hosted_zones()
    
    filtered_hosted_zone = []
    
    all_hosted_zone = response['HostedZones']
    
    for tag in all_tags:
        for zone in all_hosted_zone:
            if tag in zone['Name']:
                filtered_hosted_zone.append(zone)
    
    return filtered_hosted_zone

def get_list_of_a_records_of_hosted_zone(filtered_hosted_zone,routes):
    all_a_tag_record = []
    for data in filtered_hosted_zone:
        records = routes.list_resource_record_sets(HostedZoneId=data['Id'])
        
        # print("length:",len(records['ResourceRecordSets']))
        # print("all record:",records['ResourceRecordSets'])
        hosted_zone_record = []
        for record in records['ResourceRecordSets']:
            if record['Type'] == 'A' and data['Name'] not in record['Name']:
                hosted_zone_record.append(record)
        
        all_a_tag_record.append({
            'ID':data['Id'],
            'Record':hosted_zone_record
        })
    return all_a_tag_record

def lambda_handler(event, context):
    routes = boto3.client('route53')
    all_tags = get_list_ec2_instances_tags()
    
    
    filtered_hosted_zone = get_list_hosted_zone(all_tags,routes)
    
    
    all_unmatch_a_tag_record = get_list_of_a_records_of_hosted_zone(filtered_hosted_zone,routes)
    
    print("all_unmatch_a_tag_record: ",all_unmatch_a_tag_record)
    return {'message':'complete'}