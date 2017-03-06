""" For website comments.
"""

from sqlalchemy import (Column, DateTime, ForeignKey, String, Text,
                        Boolean, UniqueConstraint, BigInteger)
from sqlalchemy.orm import relationship, backref

from pygameweb.models import Base


class CommentCategory(Base):
    __tablename__ = 'comment_category'
    id = Column(BigInteger, primary_key=True)

    forum = Column(String(80))
    title = Column(String(80))
    order = Column(BigInteger)
    is_default = Column(Boolean)


class CommentAuthor(Base):
    __tablename__ = 'comment_author'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(80))
    email = Column(String(80))
    link = Column(String(80))
    username = Column(String(80))
    is_anonymous = Column(Boolean)
    threads = relationship('CommentThread', back_populates='author')
    posts = relationship('CommentPost', back_populates='author')

    __table_args__ = (UniqueConstraint('name',
                                       'email',
                                       # 'username',
                                       'is_anonymous',
                                       name='_name_email_is_anonymous_uc'),)

    def __repr__(self):
        return (f'<CommentAuthor({self.name}, {self.email}m {self.link}, '
                f'{self.username}, {self.is_anonymous})>')


class CommentThread(Base):
    __tablename__ = 'comment_thread'
    id = Column(BigInteger, primary_key=True)
    id_text = Column(String(255))
    forum = Column(String(255))
    category = None
    link = Column(String(255))
    """ is a URI.
    """

    title = Column(String(255))
    ip_address = Column(String(40))

    author_id = Column(BigInteger,
                       ForeignKey(CommentAuthor.id,
                                  name='comment_thread_author_id_fkey'),
                       nullable=False)
    author = relationship(CommentAuthor, back_populates='threads')

    created_at = Column(DateTime)
    is_closed = Column(Boolean)
    is_deleted = Column(Boolean)


class CommentPost(Base):
    __tablename__ = 'comment_post'
    id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger,
                       ForeignKey('comment_post.id',
                                  name='comment_post_parent_id_fkey'),
                       nullable=True)
    children = relationship('CommentPost',
                            lazy='joined',
                            backref=backref('parent', remote_side=[id]))

    thread_id = Column(BigInteger,
                       ForeignKey(CommentThread.id,
                                  name='comment_post_thread_id_fkey'),
                       nullable=False)
    thread = relationship(CommentThread)

    message = Column(Text)
    ip_address = Column(String(80))
    created_at = Column(DateTime)
    is_deleted = Column(Boolean)
    is_approved = Column(Boolean)
    is_spam = Column(Boolean)

    author_id = Column(BigInteger,
                       ForeignKey(CommentAuthor.id,
                                  name='comment_post_author_id_fkey'),
                       nullable=False)
    author = relationship(CommentAuthor, back_populates='posts')

    @classmethod
    def in_thread(cls, session, thread_id):
        """ return top level posts in thread.
        """
        parent_id = None
        is_spam = False
        is_deleted = False
        posts = (session
                 .query(CommentPost)
                 .filter(CommentPost.thread_id == thread_id)
                 .filter(CommentPost.parent_id == parent_id)
                 .filter(CommentPost.is_deleted == is_deleted)
                 .filter(CommentPost.is_spam == is_spam)
                 .order_by(CommentPost.created_at)
                 .all())
        return posts


def remove_prefix(fname):
    """This removes namespace prefix from all the things in the xml.
    """
    from lxml import etree, objectify
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(fname, parser)
    root = tree.getroot()
    for elem in root.getiterator():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i + 1:]
    objectify.deannotate(root, cleanup_namespaces=True)
    # fname_out = fname.replace('.xml', '.out.xml')
    # tree.write(fname_out,
    #            pretty_print=True,
    #            xml_declaration=True,
    #            encoding='UTF-8')
    return tree


def author_from(session, eauthor):
    """ get the author db instance from the eauthor etree tag.
    """
    eusername = eauthor.find('username')
    uname = None if eusername is None else eusername.text
    dauthor = CommentAuthor(
        email=eauthor.find('email').text,
        name=eauthor.find('name').text,
        is_anonymous=eauthor.find('isAnonymous').text == 'true',
        username=uname)

    author = (session
              .query(CommentAuthor)
              .filter(CommentAuthor.email == dauthor.email)
              .filter(CommentAuthor.name == dauthor.name)
              .filter(CommentAuthor.is_anonymous == dauthor.is_anonymous)
              .filter(CommentAuthor.username == dauthor.username)
              .first())
    if author is None:
        author = dauthor
    return author

def load_xml_threads(session, root):
    """
    """
    for thread in root.findall('thread'):
        # import pdb;pdb.set_trace()
        eauthor = thread.find('author')
        author = author_from(session, eauthor)

        # Seems all thread->authors are the owner of the forum.
        the_id = [v for k, v in thread.attrib.items() if k.endswith('id')][0]
        cthread = CommentThread(
            id=int(the_id),
            id_text=thread.find('id').text,
            forum=thread.find('forum').text,
            category=thread.find('category').text,
            link=thread.find('link').text,
            title=thread.find('title').text,
            ip_address=thread.find('ipAddress').text,
            author=author,
            created_at=thread.find('createdAt').text,
            is_closed=thread.find('isClosed').text == 'true',
            is_deleted=thread.find('isDeleted').text == 'true',
        )
        session.add(cthread)
        session.commit()


def load_xml_posts(session, root):
    """
    """
    for post in root.findall('post'):
        # import pdb;pdb.set_trace()
        eauthor = post.find('author')
        author = author_from(session, eauthor)
        session.add(author)

        the_id = [v for k, v in post.attrib.items() if k.endswith('id')][0]

        parent = post.find('parent')
        if parent is None:
            parent_id = None
        else:
            parent_id = [v for k, v in parent.attrib.items()
                         if k.endswith('id')][0]
        thread_id = [v for k, v in post.find('thread').attrib.items()
                     if k.endswith('id')][0]
        is_approved = (None if post.find('isApproved') is None
                       else post.find('isApproved').text == 'true')
        cpost = CommentPost(id=int(the_id),
                            author=author,
                            parent_id=parent_id,
                            thread_id=thread_id,
                            message=post.find('message').text,
                            ip_address=post.find('ipAddress').text,
                            created_at=post.find('createdAt').text,
                            is_deleted=post.find('isDeleted').text == 'true',
                            is_approved=is_approved,
                            is_spam=post.find('isSpam').text == 'true')
        session.add(cpost)
        session.commit()


def load_xml(session, source):
    """ Loads the xml doc into the db.
    :param session: sqlalchemy database session.
    :param source: filename, filelike, url.
    """
    tree = remove_prefix(source)
    root = tree.getroot()
    load_xml_threads(session, root)
    load_xml_posts(session, root)
