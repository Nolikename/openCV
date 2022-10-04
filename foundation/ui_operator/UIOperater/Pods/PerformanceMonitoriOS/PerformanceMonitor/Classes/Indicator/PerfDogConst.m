//
//  PerfDogConst.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/3/25.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "PerfDogConst.h"



NSString * const PerfDogIndexFps = @"fps";
NSString * const PerfDogIndexInterFrame = @"InterFrame";
NSString * const PerfDogIndexAppUsage = @"AppUsage";
NSString * const PerfDogIndexTotalUsage = @"TotalUsage";
NSString * const PerfDogIndexCpuClock = @"CpuClock";
NSString * const PerfDogIndexMemory = @"Memory";
NSString * const PerfDogIndexSwapMemory = @"SwapMemory";
NSString * const PerfDogIndexCoreUsage = @"CoreUsage";
NSString * const PerfDogIndexCpuTemperature = @"CpuTemperature";
NSString * const PerfDogIndexJank = @"Jank";
NSString * const PerfDogIndexBigJank = @"BigJank";
NSString * const PerfDogIndexDownSpeed = @"DownSpeed";
NSString * const PerfDogIndexUpSpeed = @"UpSpeed";
NSString * const PerfDogIndexRender = @"Render";
NSString * const PerfDogIndexTiler = @"Tiler";
NSString * const PerfDogIndexDevice = @"Device";
NSString * const PerfDogIndexVirtualMemory = @"VirtualMemory";
NSString * const PerfDogIndexNormalized_AppUsage = @"Normalized_AppUsage";
NSString * const PerfDogIndexNormalized_TotalUsage = @"Normalized_TotalUsage";
NSString * const PerfDogIndexNonFragmentUtilization = @"NonFragmentUtilization";
NSString * const PerfDogIndexFragmentUtilization = @"FragmentUtilization";
NSString * const PerfDogIndexAvailableMemory = @"AvailableMemory";
NSString * const PerfDogIndexGpuClock = @"GpuClock";
NSString * const PerfDogIndexGfx = @"Gfx";
NSString * const PerfDogIndexGL = @"GL";
NSString * const PerfDogIndexBusRead = @"BusRead";
NSString * const PerfDogIndexBusWrite = @"BusWrite";
NSString * const PerfDogIndexPixelThroughput = @"PixelThroughput";
NSString * const PerfDogIndexNativePss = @"NativePss";
NSString * const PerfDogIndexStutter = @"Stutter";

NSString * const CalculationMethodDiff = @"diff";
NSString * const CalculationMethodAvg = @"avg";
