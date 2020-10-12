# aliyun log alertor

framework ref https://github.com/ktlcove/kube-admission


```bash
阿里云k8s集群暂时只有日志采集插件，没有日志告警插件
此项目拓展了日志告警
由于日志采集在阿里云内安装到了 kube-system namespace 内
故此项目必须安装到 kube-system 进而从相应的configmap内读取 log-project 等参数
具体参考 values.yaml hack字段

拓展类型 AliyunLogAlertor 简称 ala


AliyunLogAlertor 示例 doc/sample-ala.yaml
spec.detail 字段内内容会原封丢给阿里云

详细字段说明参考 https://aliyun-log-python-sdk.readthedocs.io/README_CN.html#id21
详细字段如果无法满足需求 请自行 在阿里云日志告警控制台创建1个告警 然后用api把详情dump出来(阿里云售后技术支持是这么告诉我的…忍着吧)
我自己用这个推到自己的webhook 然后推企业微信机器人 所以没看其他方式怎么实现 但大同小异 自行dump配置(埋个坑 有空把机器人也搞github上来)


每一个 ala 对应 aliyun log project 内1个告警 推荐和阿里云k8s crd模式采集日志一起使用 集成自己的业务 helm chat
日志采集参考 https://help.aliyun.com/document_detail/74878.html?spm=a2c4g.11186623.2.18.907c385aQWhHH8#concept-tfg-pl1-f2b


安装：
  helm chat 在 https://github.com/ktlcove/kube-admission
  values.yaml 在项目根目录 推荐 helm3 安装



# k8s 内效果展示
kubectl get ala,aliyunlogconfig -n service
NAME                                                  AGE
aliyunlogalertor.sls.ext.aliyun.com/core-default      17d

NAME                                                      AGE
aliyunlogconfig.log.alibabacloud.com/core-file-all        14d
aliyunlogconfig.log.alibabacloud.com/core-stdout-all      14d
```