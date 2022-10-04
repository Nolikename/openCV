//
//  PerfDogConst.h
//  PerformanceMonitor
//
//  Created by 李宁 on 2022/3/25.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//
#import <Foundation/Foundation.h>

/// perfdog 指标枚举
typedef NSString *PerfDogIndex NS_STRING_ENUM;

FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexFps;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexInterFrame;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexAppUsage;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexTotalUsage;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexCpuClock;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexMemory;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexSwapMemory;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexCoreUsage;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexCpuTemperature;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexJank;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexBigJank;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexDownSpeed;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexUpSpeed;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexRender;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexTiler;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexDevice;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexVirtualMemory;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexNormalized_AppUsage;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexNormalized_TotalUsage;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexNonFragmentUtilization;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexFragmentUtilization;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexAvailableMemory;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexGpuClock;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexGfx;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexGL;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexBusRead;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexBusWrite;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexPixelThroughput;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexNativePss;
FOUNDATION_EXPORT PerfDogIndex const PerfDogIndexStutter;

/// 计算方法枚举
typedef NSString *CalculationMethod NS_STRING_ENUM;

FOUNDATION_EXPORT CalculationMethod const CalculationMethodDiff;
FOUNDATION_EXPORT CalculationMethod const CalculationMethodAvg;


