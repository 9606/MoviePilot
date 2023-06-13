from typing import Optional

from app.chain import ChainBase
from app.core.metainfo import MetaInfo
from app.core.context import Context, MediaInfo
from app.log import logger


class IdentifyChain(ChainBase):
    """
    识别处理链
    """

    def process(self, title: str, subtitle: str = None) -> Optional[Context]:
        """
        识别媒体信息
        """
        logger.info(f'开始识别媒体信息，标题：{title}，副标题：{subtitle} ...')
        # 识别前预处理
        result: Optional[tuple] = self.prepare_recognize(title=title, subtitle=subtitle)
        if result:
            title, subtitle = result
        # 识别元数据
        metainfo = MetaInfo(title, subtitle)
        # 识别媒体信息
        mediainfo: MediaInfo = self.recognize_media(meta=metainfo)
        if not mediainfo:
            logger.warn(f'{title} 未识别到媒体信息')
            return Context(meta=metainfo)
        logger.info(f'{title} 识别到媒体信息：{mediainfo.type.value} {mediainfo.title_year}')
        # 更新媒体图片
        self.obtain_image(mediainfo=mediainfo)
        # 返回上下文
        return Context(meta=metainfo, mediainfo=mediainfo, title=title, subtitle=subtitle)
