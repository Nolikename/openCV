//
//  PFTestInfo.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "PFTestInfo.h"
#import "PFAppInfo.h"
#import "PFDeviceInfo.h"

/// 测试信息
@implementation PFTestInfo

- (instancetype)initWithCaseName:(NSString *)caseName{
    if ([super init]) {
        
        self.productName = [PFAppInfo productName];
        self.caseName = caseName;
        self.appName = [PFAppInfo appName];
        self.appVersion = [PFAppInfo appVersion];
        self.appBuildNum = [[PFAppInfo appBuildVersion] integerValue];
        self.OS = [PFDeviceInfo OS];
        self.OSVersion = [PFDeviceInfo OSVersion];
        self.deviceModel = [PFDeviceInfo deviceModel];

        NSDate *currentTime = [NSDate date];
        NSTimeInterval currentTimestamp = [currentTime timeIntervalSince1970];
        self.startTime = currentTimestamp;
    }
    return  self;
}

- (void) setRecordStartTime {
    self.RecordStartTime = [PFTestInfo getTimeNow];
}

- (void) setRecordEndTime {
    self.RecordEndTime = [PFTestInfo getTimeNow];
}

+ (NSString *) getTimeNow {
    UInt64 timestamp = [[NSDate date] timeIntervalSince1970] * 1000;
    return [NSString stringWithFormat:@"%llu", timestamp];
}
@end
