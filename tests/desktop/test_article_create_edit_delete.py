#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from unittestzero import Assert
from pages.desktop.knowledge_base_new_article import KnowledgeBaseNewArticle
from pages.desktop.knowledge_base_article import KnowledgeBaseArticle
from pages.desktop.knowledge_base_article import KnowledgeBaseShowHistory
from pages.desktop.knowledge_base_article import KnowledgeBaseEditArticle
from pages.desktop.knowledge_base_article import KnowledgeBaseTranslate
from pages.desktop.login_page import LoginPage
import re
import pytest
import datetime


class TestArticleCreateEditDelete:

    def test_that_article_can_be_created(self, mozwebqa):
        """
           Creates a new knowledge base article.
           Verifies creation.
           Deletes the article
        """
        kb_new_article = KnowledgeBaseNewArticle(mozwebqa)
        kb_article_history = KnowledgeBaseShowHistory(mozwebqa)
        kb_edit_article = KnowledgeBaseEditArticle(mozwebqa)
        login_pg = LoginPage(mozwebqa)

        # Admin account is used as he can delete the article
        login_pg.log_in('admin')

        article_info_dict = self._create_new_generic_article(kb_new_article)
        kb_new_article.submit_article()
        kb_new_article.set_article_comment_box()

        # verify article history
        Assert.true(kb_article_history.is_the_current_page)

        # verify article contents
        kb_article_history.navigation.click_edit_article()

        actual_summary_text = kb_edit_article.article_summary_text
        Assert.equal(article_info_dict['summary'], actual_summary_text)

        actual_contents_text = kb_edit_article.article_contents_text
        Assert.equal(article_info_dict['content'], actual_contents_text)

        # delete the same article
        kb_edit_article.navigation.click_show_history()
        kb_article_history.delete_entire_article_document()

    @pytest.mark.xfail(reason='Bug 694614 - spurious failures')
    def test_that_article_can_be_edited(self, mozwebqa):
        """
           Creates a new knowledge base article.
           Verifies creation.
           Edits the article, verifies the edition.
           Deletes the article
        """
        kb_new_article = KnowledgeBaseNewArticle(mozwebqa)
        kb_article_history = KnowledgeBaseShowHistory(mozwebqa)
        kb_edit_article = KnowledgeBaseEditArticle(mozwebqa)
        login_pg = LoginPage(mozwebqa)

        # Admin account is used as he can delete the article
        login_pg.log_in('admin')

        article_info_dict = self._create_new_generic_article(kb_new_article)
        kb_new_article.submit_article()
        kb_new_article.set_article_comment_box()

        # verify article history
        Assert.true(kb_article_history.is_the_current_page)

        # edit that same article
        timestamp = datetime.datetime.now()
        edited_article_summary = "this is an automated summary__%s_edited" % timestamp
        edited_article_content = "automated content__%s_edited" % timestamp
        article_info_dict_edited = {'title': article_info_dict['title'],\
                                    'category': 'How to', 'keyword': 'test',\
                                    'summary': edited_article_summary, 'content': edited_article_content}

        kb_article_history.navigation.click_edit_article()
        kb_edit_article.edit_article(article_info_dict_edited)

        kb_article_history.navigation.click_edit_article()

        # verify the contents of the edited article
        actual_page_title = kb_edit_article.page_title
        Assert.contains(article_info_dict_edited['title'], actual_page_title)

        actual_summary_text = kb_edit_article.article_summary_text
        Assert.equal(edited_article_summary, actual_summary_text)

        actual_content_text = kb_edit_article.article_contents_text
        Assert.equal(edited_article_content, actual_content_text)

        # delete the same article
        kb_edit_article.navigation.click_show_history()
        kb_article_history.delete_entire_article_document()

    def test_that_article_can_be_deleted(self, mozwebqa):
        """
           Creates a new knowledge base article.
           Deletes the article.
           Verifies the deletion.
        """
        kb_new_article = KnowledgeBaseNewArticle(mozwebqa)
        kb_article = KnowledgeBaseArticle(mozwebqa)
        kb_article_history = KnowledgeBaseShowHistory(mozwebqa)
        login_pg = LoginPage(mozwebqa)

        # Admin account is used as he can delete the article
        login_pg.log_in('admin')

        article_info_dict = self._create_new_generic_article(kb_new_article)

        kb_new_article.submit_article()
        kb_new_article.set_article_comment_box()

        # go to article and get URL
        kb_article_history.navigation.click_article()
        article_url = kb_article.url_current_page

        # delete the same article
        kb_article.navigation.click_show_history()
        kb_article_history.delete_entire_article_document()

        kb_article_history.selenium.get(article_url)
        actual_page_title = kb_article_history.page_title
        Assert.contains("Page Not Found", actual_page_title)

    def test_that_article_can_be_previewed_before_submitting(self, mozwebqa):

        kb_new_article = KnowledgeBaseNewArticle(mozwebqa)
        login_pg = LoginPage(mozwebqa)

        # Admin account is used as he can delete the article
        login_pg.log_in('admin')

        article_info_dict = self._create_new_generic_article(kb_new_article)

        kb_new_article.click_article_preview_button()
        actual_preview_text = kb_new_article.article_preview_text

        Assert.equal(article_info_dict['content'], actual_preview_text)

        # Does not need to be deleted as it does not commit the article

    def test_that_article_can_be_translated(self, mozwebqa):
        """
           Creates a new knowledge base article.
           Translate article
        """
        kb_new_article = KnowledgeBaseNewArticle(mozwebqa)
        kb_article_history = KnowledgeBaseShowHistory(mozwebqa)
        kb_edit_article = KnowledgeBaseEditArticle(mozwebqa)
        kb_translate_pg = KnowledgeBaseTranslate(mozwebqa)
        login_pg = LoginPage(mozwebqa)
        timestamp = datetime.datetime.now()

        # Admin account is used as he can delete the article
        login_pg.log_in('admin')

        article_info_dict = self._create_new_generic_article(kb_new_article)
        kb_new_article.submit_article()
        kb_new_article.set_article_comment_box()

        # verify article history
        Assert.true(kb_article_history.is_the_current_page)

        kb_article_history.navigation.click_translate_article()
        kb_translate_pg.click_translate_language('Esperanto (eo)')

        kb_translate_pg.type_title('artikolo_titolo%s' % timestamp)
        kb_translate_pg.type_slug('artikolo_limako_%s' % timestamp)
        kb_translate_pg.click_submit_review()

        change_comment = 'artikolo sangoj %s' % timestamp
        kb_translate_pg.type_modal_describe_changes(change_comment)
        kb_translate_pg.click_modal_submit_changes_button()

        Assert.equal(change_comment, kb_article_history.most_recent_revision_comment)
        Assert.equal('Esperanto', kb_article_history.revision_history)

        kb_article_history.delete_entire_article_document()

    def _create_new_generic_article(self, kb_new_article):
        timestamp = datetime.datetime.now()

        article_name = "test_article_%s" % timestamp
        article_summary = "this is an automated summary_%s" % timestamp
        article_content = "automated content_%s" % timestamp

        article_info_dict = {'title': article_name,
                             'category': 'How to', 'keyword': 'test',
                             'summary': article_summary, 'content': article_content}

        # create a new article
        kb_new_article.go_to_create_new_article_page()
        kb_new_article.set_article(article_info_dict)

        return article_info_dict
