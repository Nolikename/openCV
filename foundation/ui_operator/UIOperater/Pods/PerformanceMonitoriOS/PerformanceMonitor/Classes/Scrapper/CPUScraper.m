//
//  NPTCPUScraper.m
//  Performance
//
//  Created by Iansl on 2019/6/10.
//  Copyright © 2019 Tencent. All rights reserved.
//

#import "CPUScraper.h"
#import <mach/task.h>
#import <mach/vm_map.h>
#import <mach/mach_init.h>
#import <mach/thread_act.h>
#import <mach/thread_info.h>

/// CPU追踪器
@interface CPUScraper()

/// 追踪过程中cpu的值[1,2,3,4,5]
@property(nonatomic, copy) NSString *cpuValue;

/// cpu的cpu的最大值
@property(nonatomic, assign) double cpuMax;

@end

/// CPU追踪器
@implementation CPUScraper

+ (double)getCpuUsage {
    kern_return_t kr;
       ///任务信息
       task_info_data_t tinfo;
       ///任务个数
       mach_msg_type_number_t task_info_count;
       ///最大1024
       task_info_count = TASK_INFO_MAX;
       ///获取当前执行的任务信息和个数
       kr = task_info(mach_task_self(), TASK_BASIC_INFO, (task_info_t)tinfo, &task_info_count);
       ///判断是否获取成功
       if (kr != KERN_SUCCESS) {
           return -1;
       }
       /// 基础任务
       task_basic_info_t      basic_info;
       /// 线程数组
       thread_array_t        thread_list;
       /// 线程个数
       mach_msg_type_number_t thread_count;
       /// 线程信息
       thread_info_data_t    thinfo;
       /// 线程信息个数
       mach_msg_type_number_t thread_info_count;
       /// 基础线程信息
       thread_basic_info_t basic_info_th;
       /// 存储运行的线程
       uint32_t stat_thread = 0;
       
       basic_info = (task_basic_info_t)tinfo;
       /// 获取当前执行的线程数组和个数
       kr = task_threads(mach_task_self(), &thread_list, &thread_count);
       /// 判断是否成功
       if (kr != KERN_SUCCESS) {
           return -1;
       }
       
       if (thread_count > 0) {
           stat_thread += thread_count; 
       }
       long tot_sec = 0; 
       long tot_usec = 0;
       float tot_cpu = 0;
       int j;
       ///遍历所有线程
       for (j = 0; j < (int)thread_count; j++) {
           ///线程信息最大个数
           thread_info_count = THREAD_INFO_MAX;
           ///获取线程的基础信息和信息个数
           kr = thread_info(thread_list[j], THREAD_BASIC_INFO,
                            (thread_info_t)thinfo, &thread_info_count);
           ///判断是否成功
           if (kr != KERN_SUCCESS) {
               return -1;
           }
           ///转换基础信息类型
           basic_info_th = (thread_basic_info_t)thinfo;
           ///判断不是闲置线程信息
           if (!(basic_info_th->flags & TH_FLAGS_IDLE)) {
               ///使用时间计算
               tot_sec = tot_sec + basic_info_th->user_time.seconds + basic_info_th->system_time.seconds;
               tot_usec = tot_usec + basic_info_th->user_time.microseconds + basic_info_th->system_time.microseconds;
               ///使用率计算
               tot_cpu = tot_cpu + basic_info_th->cpu_usage / (float)TH_USAGE_SCALE * 100.0;
           }
       }
       ///释放指针
       kr = vm_deallocate(mach_task_self(), (vm_offset_t)thread_list, thread_count * sizeof(thread_t));
       ///成功
       assert(kr == KERN_SUCCESS);
        
        // 容错，CPU占用率不允许是负数
        float final = roundf(tot_cpu);
        if (final < 0) {
            final = 0;
        }
       ///返回CPU使用率
       return final;
}

#pragma mark - NPTScraperProtocal
- (NSDictionary *)grabTraceData {
    double cpuUsage = [[self class] getCpuUsage]; 
    if (self.cpuValue) {
        self.cpuValue = [NSString stringWithFormat:@"%@,%.2lf", self.cpuValue, cpuUsage];
    } else {
        self.cpuValue = [NSString stringWithFormat:@"%.2lf", cpuUsage];
    }
    if (self.cpuMax < cpuUsage) {
        self.cpuMax = cpuUsage;
    }
    NSLog(@"------------%@", @{@"CPU": @(cpuUsage)});
    return @{@"cpu": @([[self class] getCpuUsage])};
}

@end
