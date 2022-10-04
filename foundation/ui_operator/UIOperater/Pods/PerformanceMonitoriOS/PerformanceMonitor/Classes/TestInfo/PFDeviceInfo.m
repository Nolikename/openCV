//
//  PFDeviceInfo.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "PFDeviceInfo.h"
#include <sys/sysctl.h>
#import <sys/utsname.h>


/// 设备信息
@implementation PFDeviceInfo

/// 操作系统 IPH/AND
+ (NSString *)OS {
    return @"IPH";
}

/// 操作系统版本
+ (NSString *)OSVersion {
    return [[UIDevice currentDevice] systemVersion];
}

/// 手机版本iPhone12 pro max
+ (NSString *)deviceModel {
    NSString *platform = [PFDeviceInfo platform];
    NSDictionary *machineMap = [PFDeviceInfo machineMap];
    NSString *deviceModel = [machineMap objectForKey:platform];
    if (!deviceModel) {
        deviceModel = @"unknow device";
    }
    return deviceModel;
}

/// 汇总OS、OSVersion、deviceModel等信息
+ (NSDictionary *)dicForBaseParam {
    return @{@"OS": [self OS], @"OSVer": [self OSVersion], @"device": [self deviceModel]};
}

+ (NSString *)platform {
    struct utsname systemInfo;
    uname(&systemInfo);
    NSString *platform = [NSString stringWithCString: systemInfo.machine encoding:NSASCIIStringEncoding];
    return platform;
}

+ (NSDictionary<NSString *, NSString *> *)machineMap {
    return @{
        @"iPhone1,1": @"iPhone",
        @"iPhone1,2": @"iPhone 3G",
        @"iPhone2,1": @"iPhone 3GS",
        @"iPhone3,1": @"iPhone 4",
        @"iPhone3,2": @"iPhone 4",
        @"iPhone3,3": @"iPhone 4",
        @"iPhone4,1": @"iPhone 4s",
        @"iPhone5,1": @"iPhone 5",
        @"iPhone5,2": @"iPhone 5",
        @"iPhone5,3": @"iPhone 5c",
        @"iPhone5,4": @"iPhone 5c",
        @"iPhone6,1": @"iPhone 5s",
        @"iPhone6,2": @"iPhone 5s",
        @"iPhone7,1": @"iPhone 6 Plus",
        @"iPhone7,2": @"iPhone 6",
        @"iPhone8,1": @"iPhone 6s",
        @"iPhone8,2": @"iPhone 6s Plus",
        @"iPhone8,4": @"iPhone SE",
        @"iPhone9,1": @"iPhone 7",
        @"iPhone9,3": @"iPhone 7",
        @"iPhone9,2": @"iPhone 7 Plus",
        @"iPhone9,4": @"iPhone 7 Plus",
        @"iPhone10,1": @"iPhone 8",
        @"iPhone10,4": @"iPhone 8",
        @"iPhone10,2": @"iPhone 8 Plus",
        @"iPhone10,5": @"iPhone 8 Plus",
        @"iPhone10,3": @"iPhone X",
        @"iPhone10,6": @"iPhone X",
        @"iPhone11,2": @"iPhone XS",
        @"iPhone11,4": @"iPhone XS Max",
        @"iPhone11,6": @"iPhone XS Max",
        @"iPhone11,8": @"iPhone XR",
        @"iPhone12,1": @"iPhone 11",
        @"iPhone12,3": @"iPhone 11 Pro",
        @"iPhone12,5": @"iPhone 11 Pro Max",
        @"iPhone12,8": @"iPhone SE2",
        @"iPhone13,1": @"iPhone 12 mini",
        @"iPhone13,2": @"iPhone 12",
        @"iPhone13,3": @"iPhone 12 Pro",
        @"iPhone13,4": @"iPhone 12 Pro Max",
        @"i386": @"iPhone Simulator",
        @"x86_64": @"iPhone Simulator"
    };
}

+ (NSInteger)cpuNum{
    unsigned int ncpu;
    size_t len = sizeof(ncpu);
    sysctlbyname("hw.ncpu", &ncpu, &len, NULL, 0);
    NSInteger cpuNum = ncpu;
    return cpuNum;
}

@end
