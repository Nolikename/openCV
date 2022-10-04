//
//  NPTMemScraper.m
//  NextTestTests
//
//  Created by BenArvin on 2019/6/15.
//  Copyright © 2019 Qzone_test. All rights reserved.
//

#import "MemScraper.h"
#import <mach/task.h>
#import <mach/mach.h>
#import <mach/mach_init.h>
#import <UIKit/UIKit.h>

/// 内存追踪器
@interface MemScraper()
/// 是第一次开始追踪么
@property (atomic) BOOL isFirstScrape;
/// 内存的值
@property (nonatomic, copy) NSString *memValue;
/// 测试过程中最大的内存值
@property (atomic) CGFloat footprintMemMax;
@end

/// 内存追踪器
@implementation MemScraper

- (instancetype)init {
    self = [super init];
    if (self) {
        _memValue = @"";
    }
    return self;
}

+ (float)grabMemoryInfo {
    float footprintMem = 0.0;
    CGFloat residentMem = 0.0;
    
    task_vm_info_data_t vmInfo;
    mach_msg_type_number_t count = TASK_VM_INFO_COUNT;
    kern_return_t kr = task_info(mach_task_self(), TASK_VM_INFO, (task_info_t) &vmInfo, &count);
    mach_task_basic_info_data_t taskInfo;
    mach_msg_type_number_t      task_basic_info_count = MACH_TASK_BASIC_INFO_COUNT;
    kern_return_t               kernReturn = task_info(mach_task_self(),
                                                       MACH_TASK_BASIC_INFO,
                                                       (task_info_t)&taskInfo,
                                                       &task_basic_info_count);
    if(kr != KERN_SUCCESS) {
        footprintMem = 0;
    } else {
        footprintMem = vmInfo.phys_footprint / 1024.0 / 1024.0;
    }
    
    if (kernReturn != KERN_SUCCESS) {
        residentMem = 0.0;
    } else {
        residentMem = taskInfo.resident_size / 1024.0 / 1024.0;
    }
    NSMutableDictionary *result = [[NSMutableDictionary alloc] init];
    [result setObject:@(footprintMem) forKey:@"MEM"]; 
//    [result setObject:@(residentMem) forKey:@"residentMem"];
    return footprintMem;
}

#pragma mark - NPTScraperProtocal


- (void)startScrape {
    self.footprintMemMax = 0.0;
    self.isFirstScrape = YES;
    self.memValue = @"";
}

@end
