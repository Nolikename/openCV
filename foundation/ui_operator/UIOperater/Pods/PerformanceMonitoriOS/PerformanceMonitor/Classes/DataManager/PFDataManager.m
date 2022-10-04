//
//  DataManager.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "PFDataManager.h"
#import "EPDefine.h"

/// 性能数据写入器
@interface PFDataManager ()
/// 测试基础信息模型
@property (nonatomic)PFTestInfo *testInfo;

/// 日期格式
@property (nonatomic) NSDateFormatter *dataFormatter;

/// 是不是第一次记录
@property (nonatomic) BOOL firstRecord;

/// 文件路径
@property (nonatomic) NSString *filePath;

/// 临时文件路径
@property (nonatomic) NSString *tmpFilePath;

/// 文件处理器
@property (nonatomic) NSFileHandle *fileHandle;//TODO: nds，需改为NSStream方式，避免NSFileHandle导致的内存暴涨问题

@end

/// 性能数据写入器
@implementation PFDataManager
- (instancetype)initWithCaseName:(NSString *)caseName{
    self = [super init];
    if (self) {
        PFTestInfo *testInfo = [[PFTestInfo alloc] initWithCaseName:caseName];
        self.testInfo = testInfo;
        [self deleteTmpDir];
        [PFDataManager createTrailFolderIfNeed];
        NSDate *currentTime = [NSDate date];
        _filePath = [self buildFilePath:currentTime];
        _tmpFilePath = [self buildTmpFilePath:currentTime];
        
        BOOL isDirectory;
        BOOL exists = [[NSFileManager defaultManager] fileExistsAtPath:_filePath isDirectory:&isDirectory];
        if (exists && !isDirectory) {
            [[NSFileManager defaultManager] removeItemAtPath:_filePath error:nil];
        }
        
        [[NSFileManager defaultManager] createFileAtPath:_filePath contents:nil attributes:nil];
        _fileHandle = [NSFileHandle fileHandleForUpdatingAtPath:_filePath];
        
        _firstRecord = YES;
    }
    return self;
}


- (void)dealloc {
    if (_fileHandle) {
        [_fileHandle synchronizeFile];
        [_fileHandle closeFile];
    }
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _dataFormatter = [[NSDateFormatter alloc] init];
        [_dataFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss.SSSXXX"];
    }
    return self;
}

#pragma mark - public methods
- (void)writeToSandBox:(NSArray *)arr{
    [self recordDetailData:arr];
    [self recordBaseParamAndAdditionalInfo];
    [[NSFileManager defaultManager] copyItemAtPath:self.filePath toPath:self.tmpFilePath error:nil];
}

-(void)deleteTmpDir{
    NSString *folderPath = [PFDataManager tmpTrailFolderPath];
    BOOL isDirectory;
    BOOL exists = [[NSFileManager defaultManager] fileExistsAtPath:folderPath isDirectory:&isDirectory];
    if (exists && isDirectory) {
        [[NSFileManager defaultManager] removeItemAtPath:folderPath error:nil];
    }
}

+ (void)cleanAllTraceFile {
    NSString *folderPath = [self trailFolderPath];
    BOOL isDirectory;
    BOOL exists = [[NSFileManager defaultManager] fileExistsAtPath:folderPath isDirectory:&isDirectory];
    if (exists && isDirectory) {
        [[NSFileManager defaultManager] removeItemAtPath:folderPath error:nil];
    }
    [self createTrailFolderIfNeed];
}

+ (NSString *)dicPairToString:(NSString *)key value:(id)value {
    if ([value isKindOfClass:[NSNumber class]]) {
        if ([key isEqualToString:@"Threshold"] ||[key isEqualToString:@"ComparisonMode"] ||[key isEqualToString:@"ThresholdUp"] ||[key isEqualToString:@"ThresholdDown"]||[key isEqualToString:@"HideChat"]) {
            // EPTest平台上threshold只支持整型数据
            return [NSString stringWithFormat:@"\"%@\":%d", key, ((NSNumber *)value).intValue];
        }else{
            return [NSString stringWithFormat:@"\"%@\":%f", key, ((NSNumber *)value).doubleValue];
        }
        
    } else {
        return [NSString stringWithFormat:@"\"%@\":\"%@\"", key, value];
    }
}

#pragma mark - private methods
+ (NSString *)documentsPath {
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    return [paths firstObject];
}

+ (NSString *)tmpTrailFolderPath {
    return [[NSString stringWithFormat:@"%@/NPTTrail/tmp/", [self documentsPath]] stringByReplacingOccurrencesOfString:@"//" withString:@"/"];
}

+ (NSString *)trailFolderPath {
    return [[NSString stringWithFormat:@"%@/NPTTrail/",
             [self documentsPath]] stringByReplacingOccurrencesOfString:@"//" withString:@"/"];
}

- (NSString *)buildFilePath:(NSDate *)time {
    return [[NSString stringWithFormat:@"%@/%@-%.9f",
             [[self class] trailFolderPath],
             self.testInfo.caseName,
             [time timeIntervalSince1970]] stringByReplacingOccurrencesOfString:@"//" withString:@"/"];
}

- (NSString *)buildTmpFilePath:(NSDate *)time {
    return [[NSString stringWithFormat:@"%@/%@-%.9f",
             [[self class] tmpTrailFolderPath],
             self.testInfo.caseName, [time timeIntervalSince1970]]
            stringByReplacingOccurrencesOfString:@"//" withString:@"/"];
}

+ (void)createTrailFolderIfNeed {
    NSString *folderPath = [self tmpTrailFolderPath];
    BOOL isDirectory;
    BOOL exists = [[NSFileManager defaultManager] fileExistsAtPath:folderPath isDirectory:&isDirectory];
    if (!exists || !isDirectory) {
        [[NSFileManager defaultManager] createDirectoryAtPath:folderPath withIntermediateDirectories:YES attributes:nil error:nil];
    }
}

- (void)recordDetailData:(NSArray *)addtionalDataArray {
    
    NSString *caseConclusion = [self caseConclusion:addtionalDataArray];
    
    [self.fileHandle writeData:[[NSString stringWithFormat:@"\"Conclusion\":\"%@\",", caseConclusion] dataUsingEncoding:NSUTF8StringEncoding]];
    // ------ detail字段开始 ------
    [self.fileHandle writeData:[@"\"Detail\":[{" dataUsingEncoding:NSUTF8StringEncoding]];
    [self.fileHandle writeData:[[NSString stringWithFormat:@"\"CaseName\":\"%@\",",self.testInfo.caseName] dataUsingEncoding:NSUTF8StringEncoding]];
    [self.fileHandle writeData:[[NSString stringWithFormat:@"\"Conclusion\":\"%@\",",caseConclusion] dataUsingEncoding:NSUTF8StringEncoding]];
    
    //------------- result 字段开始 -------------
    if (addtionalDataArray && addtionalDataArray.count > 0) {
        [self.fileHandle writeData:[@"\"Result\":[" dataUsingEncoding:NSUTF8StringEncoding]];
        
        for (int i = 0; i<addtionalDataArray.count; i++) {
            [self.fileHandle writeData:[@"{" dataUsingEncoding:NSUTF8StringEncoding]];
            NSDictionary *dic = addtionalDataArray[i];
           
            NSInteger count = dic.count;
            NSInteger index = 1;
            
            for (NSString *key in [dic allKeys]) {
                if ([key isEqual:@"TestStageList"]) {
                    [self recordCaseStageInfo:[dic objectForKey:key]];
                } else {
                    [self.fileHandle writeData:[[[self class] dicPairToString:key value:[dic objectForKey:key]]
                                                dataUsingEncoding:NSUTF8StringEncoding]];
                }
                if (index < count) {
                    [self.fileHandle writeData:[@"," dataUsingEncoding:NSUTF8StringEncoding]];
                }
                index++;
            }
            
            if (i == addtionalDataArray.count - 1) {
                [self.fileHandle writeData:[@"}" dataUsingEncoding:NSUTF8StringEncoding]];
            }else{
                [self.fileHandle writeData:[@"}," dataUsingEncoding:NSUTF8StringEncoding]];
            }
        }
        [self.fileHandle writeData:[@"]" dataUsingEncoding:NSUTF8StringEncoding]];
    }
    //------------- result 字段结束 -------------
    
    [self.fileHandle writeData:[@"}]" dataUsingEncoding:NSUTF8StringEncoding]];
    // ------ detail字段结束 ------

    [self.fileHandle writeData:[@"}" dataUsingEncoding:NSUTF8StringEncoding]];
    [self.fileHandle synchronizeFile];
}

- (void)recordCaseStageInfo:(NSDictionary *)testStageList{
    [self.fileHandle writeData:[@"\"TestStageList\":[" dataUsingEncoding:NSUTF8StringEncoding]];
    int i = 0;
    for(id stageIndex in testStageList) {
        Stage *stage = [testStageList objectForKey:stageIndex];
        NSDictionary *dic = [stage getStage];
        NSInteger count = dic.count;
        NSInteger index = 1;
        
        [self.fileHandle writeData:[@"{" dataUsingEncoding:NSUTF8StringEncoding]];
        for(id key in dic) {
            [self.fileHandle writeData:[[[self class] dicPairToString:key value:[dic objectForKey:key]] dataUsingEncoding:NSUTF8StringEncoding]];
            if (index < count) {
                [self.fileHandle writeData:[@"," dataUsingEncoding:NSUTF8StringEncoding]];
            }
            index++;
        }
        
        if (i == testStageList.count - 1) {
            [self.fileHandle writeData:[@"}" dataUsingEncoding:NSUTF8StringEncoding]];
        } else {
            [self.fileHandle writeData:[@"}," dataUsingEncoding:NSUTF8StringEncoding]];
        }
        i++;
    }
    [self.fileHandle writeData:[@"]" dataUsingEncoding:NSUTF8StringEncoding]];
}

- (void)recordBaseParamAndAdditionalInfo {
    NSMutableString *tmpString = [NSMutableString stringWithString:@"{"];
    [tmpString appendString:[NSString stringWithFormat:@"\"ProductName\":\"%@\",", self.testInfo.productName]];
    [tmpString appendString:[NSString stringWithFormat:@"\"OS\":\"%@\",", self.testInfo.OS]];
    [tmpString appendString:[NSString stringWithFormat:@"\"OSVer\":\"%@\",", self.testInfo.OSVersion]];
    [tmpString appendString:[NSString stringWithFormat:@"\"AppName\":\"%@\",", self.testInfo.appName]];
    [tmpString appendString:[NSString stringWithFormat:@"\"AppVersion\":\"%@\",", self.testInfo.appVersion]];
    [tmpString appendString:[NSString stringWithFormat:@"\"AppBuildNum\":%d,", (int)self.testInfo.appBuildNum]];
    [tmpString appendString:[NSString stringWithFormat:@"\"DeviceName\":\"%@\",", self.testInfo.deviceModel]];
    [tmpString appendString:[NSString stringWithFormat:@"\"VideoKey\":\"%@\",", @""]];
    if (![self.testInfo.RecordStartTime isEqual: @""] &&
        ![self.testInfo.RecordEndTime isEqual: @""]) {
        [tmpString appendString:[NSString stringWithFormat:@"\"RecordStartTime\":\"%@\",", self.testInfo.RecordStartTime]];
        [tmpString appendString:[NSString stringWithFormat:@"\"RecordEndTime\":\"%@\",", self.testInfo.RecordEndTime]];
    }
    [self insertAtFileStart:tmpString];
}

- (void)insertAtFileStart:(NSString *)content {
    [self.fileHandle seekToFileOffset:0];
    NSData *oldData = [self.fileHandle readDataToEndOfFile];
    [self.fileHandle seekToFileOffset:0];
    if (!oldData) {
        [self.fileHandle writeData:[content dataUsingEncoding:NSUTF8StringEncoding]];
        [self.fileHandle synchronizeFile];
        return;
    }
    NSString *oldString = [[NSString alloc] initWithData:oldData encoding:NSUTF8StringEncoding];
    [self.fileHandle writeData:[[NSString stringWithFormat:@"%@%@", content, oldString] dataUsingEncoding:NSUTF8StringEncoding]];
    [self.fileHandle synchronizeFile];
}

// 获取测试用例是否通过
- (NSString *)caseConclusion:(NSArray *)addtionalDataArray{
    NSString *caseConclusion = PASS;
    for (NSDictionary *dic in addtionalDataArray) {
        NSString *conclusion = dic[@"conclusion"];
        if ([conclusion isEqualToString:@"fail"]) {
            caseConclusion = @"fail";
        }
    }
    return caseConclusion;
}

- (void)setRecordStartTime {
    [self.testInfo setRecordStartTime];
}

- (void)setRecordEndTime {
    [self.testInfo setRecordEndTime];
}

@end
